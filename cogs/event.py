from discord.ext.commands import Cog, Bot


class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} is now online")


def setup(bot):
    bot.add_cog(Events(bot))
