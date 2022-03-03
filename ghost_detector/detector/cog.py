from collections import defaultdict
import csv
from dataclasses import dataclass, field
import datetime as dt
from io import StringIO
import logging
from typing import Literal, Optional, TextIO, cast

import discord
from discord import Member
from discord.ext import commands

from slugify import slugify

__all__ = [
    'Detector'
]

logger = logging.getLogger('ghost_detector.detector')


class ProgressMessage:

    progress_emojis = {
        'idle': ':white_medium_square:',
        'in_progress': ':arrow_right:',
        'done': ':white_check_mark:',
        'error': ':warning:'
    }

    def __init__(self, messageable: discord.abc.Messageable, items: list[str]):
        self.messageable = messageable
        self.items = {i: 'idle' for i in items}
        self._msg: Optional[discord.Message] = None

    def __str__(self):
        return '\n'.join(
            (f'{self.progress_emojis[status]} {i}' for i, status in self.items.items())
        )

    @property
    def message(self) -> Optional[discord.Message]:
        return self._msg

    async def set_status(
            self, item: str, status: Literal['idle', 'in_progress', 'done', 'error']
    ):
        self.items[item] = status

    async def update(self):
        if self._msg is None:
            self._msg = await self.messageable.send(str(self))
        else:
            await self._msg.edit(content=str(self))


@dataclass
class UserInfo:
    msg_count: int = 0
    last_msg_date: dt.datetime = field(default_factory=lambda: dt.datetime(1, 1, 1))


class Detector(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _get_visible_channels(self, guild: discord.Guild):
        channels = []
        for channel in guild.text_channels:
            perms = channel.permissions_for(guild.me)
            if perms.view_channel and perms.read_message_history:
                channels.append(channel)
        return channels

    def _create_csv(
            self, users: dict[Member, UserInfo], max_count: int
    ) -> tuple[TextIO, TextIO]:
        """
        :return: a tuple of CSV text streams of (pruned_users, all_users)
        """
        def write_row(writer: csv.writer, member: Member, info: UserInfo):
            writer.writerow([
                f'{member.name}#{member.discriminator}',
                member.id,
                member.display_name,
                info.msg_count,
                member.joined_at,
                info.last_msg_date,
                ', '.join(sorted(r.name for r in member.roles if r.name != '@everyone'))
            ])

        ghost_users = cast(
            list[tuple[Member, UserInfo]],
            sorted(list(users.items()), key=lambda u: u[0].name)
        )

        cols = [
            'user', 'id', 'nickname', 'message_count', 'joined_at',
            'last_message_date', 'roles'
        ]
        csv_pruned_stream = StringIO()
        csv_pruned_writer = csv.writer(csv_pruned_stream)
        csv_pruned_writer.writerow(cols)
        csv_all_stream = StringIO()
        csv_all_writer = csv.writer(csv_all_stream)
        csv_all_writer.writerow(cols)

        for member, info in ghost_users:
            try:
                write_row(csv_all_writer, member, info)
                if info.msg_count != max_count:
                    write_row(csv_pruned_writer, member, info)
            except Exception as e:
                logger.error(f"Error while writing CSV row for user {member}", exc_info=e)

        csv_pruned_stream.seek(0)
        csv_all_stream.seek(0)
        return csv_pruned_stream, csv_all_stream

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def detect(self, context: commands.Context, max_count: int = 50):
        async with context.typing():
            await self._do_detect(context, max_count)

    async def _do_detect(self, context: commands.Context, max_count: int):
        channels = await self._get_visible_channels(context.guild)
        users: defaultdict[Member, UserInfo] = defaultdict(UserInfo)

        progress = ProgressMessage(context, [c.name for c in channels])
        await progress.update()

        # Iterate through every message in every channel and collect the data
        for channel in channels:
            channel: discord.TextChannel
            await progress.set_status(channel.name, 'in_progress')
            await progress.update()

            try:
                async for msg in channel.history(limit=None, oldest_first=True):
                    if msg.author.bot or not isinstance(msg.author, Member):
                        # User left the server
                        continue
                    msg: discord.Message
                    user_info = users[msg.author]
                    if user_info.msg_count < max_count:
                        # Only count up to the max for privacy reasons
                        user_info.msg_count += 1
                    if msg.created_at > user_info.last_msg_date:
                        user_info.last_msg_date = msg.created_at

            except Exception as e:
                logger.error(
                    f"Error while detecting ghosts (channel={channel.name})",
                    exc_info=e
                )
                await progress.set_status(channel.name, 'error')
            else:
                await progress.set_status(channel.name, 'done')

        await progress.update()

        pruned_csv, all_csv = self._create_csv(users, max_count)
        guild_slug = slugify(context.guild.name, separator="_", lowercase=False)
        now_ts = dt.datetime.utcnow().strftime("%Y%m%d_%H%M")
        files = [
            discord.File(pruned_csv, f'GhostUsers_{guild_slug}_{now_ts}_PRUNED.csv'),
            discord.File(all_csv, f'GhostUsers_{guild_slug}_{now_ts}_ALL.csv')
        ]
        await context.send(files=files)
