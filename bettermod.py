#!/bin/python
from database import database
from util import check_for_token, add_cogs

from discord.ext.commands import AutoShardedBot
from discord.ext.commands.errors import MissingRequiredArgument, MemberNotFound
from discord.ext.commands import Context
from discord.embeds import Embed
from discord.colour import Color

from cogs.moderation import Moderation
from cogs.debug import Debugging

check_for_token()

bot: AutoShardedBot = AutoShardedBot("--")


@bot.event
async def on_ready():
    print(bot.user.name + " is now online.\n")


@bot.event
async def on_command_error(ctx: Context, error):
    embed = Embed(color=Color(0xff0000))

    if isinstance(error, MissingRequiredArgument):

        syntax: str = ctx.command.help.split("\n")[1]
        syntax = syntax.replace("member", "member (mention | user id)")

        embed.add_field(name="Syntax",
                        value=f"`{await ctx.bot.get_prefix(ctx)}{ctx.command.name} {syntax}`")

        embed.add_field(name="Symbol explanation",
                        value="`<...>` - Required argument\n`[...]` - Optional argument\n`(...)` - explanation\n`|` - or",
                        inline=False)

    elif isinstance(error, MemberNotFound):
        embed.description = "Member `" + error.argument + "` not found"
    else:
        embed.add_field(name="Unknown error", value=error)

    await ctx.send(embed=embed)


add_cogs(bot, Debugging, Moderation)
bot.run(database.get_token())
