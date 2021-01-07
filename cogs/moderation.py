from discord.ext.commands import Cog, Bot


class Moderation(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot


def setup(bot):
    bot.add_cog(Moderation(bot))
