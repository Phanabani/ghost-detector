from discord.ext.commands import Bot

from .cog import Detector


def setup(bot: Bot):
    bot.add_cog(Detector(bot))
