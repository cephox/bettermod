from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog, Context, CommandNotFound, MissingPermissions

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
                            value="** **", inline=False)
        elif isinstance(error, MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '`{}` ' + lang.add + ' `{}`'.format(", ".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(["`" + i + "`" for i in missing])
            embed.add_field(name=lang.error_missing_permissions, value=fmt, inline=False)
        else:
            embed.add_field(name=lang.error_unknown, value=str(error), inline=False)
            embed.add_field(name=lang.error_debug_information, value=str(type(error)), inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Errors(Cog))
