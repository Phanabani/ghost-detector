import logging

import discord
from discord.ext import commands

__all__ = [
    'MyCog'
]

logger = logging.getLogger('ghost_detector.my_extension')


class MyCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
