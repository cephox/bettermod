from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog, Context, CommandNotFound

from colors import Colors
from translation import get_user_language


class Errors(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        lang = get_user_language(ctx.author.id)
        embed = Embed(color=Colors.error, timestamp=datetime.now())

        if isinstance(error, CommandNotFound):
            print(error)
            embed.add_field(name=lang.f_error_command_not_found("`" + str(error).split(" ")[1].replace("\"", "") + "`"),
                            value="** **")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Errors(Cog))
