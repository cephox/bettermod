#!/bin/python
from discord.embeds import Embed
from discord.ext.commands import AutoShardedBot
from discord.ext.commands import Context
from discord.ext.commands.errors import MissingRequiredArgument, MemberNotFound, MissingPermissions

import logger
from cogs.events import Events
from cogs.moderation import Moderation
from cogs.settings import Settings
from colours import Colours
from database import database
from util import check_for_token, add_cogs

check_for_token()

bot: AutoShardedBot = AutoShardedBot("--")


@bot.event
async def on_ready():
    print(bot.user.name + " is now online.\n")


@bot.event
async def on_command_error(ctx: Context, error):
    embed = Embed(color=Colours.red)

    if isinstance(error, MissingRequiredArgument):

        syntax: str = ctx.command.help.split("\n")[1]
        syntax = syntax.replace("member", "member (mention | user id)")
        syntax = syntax.replace("textchannel", "textchannel (mention | channel id)")

        embed.add_field(name="Syntax",
                        value=f"`{await ctx.bot.get_prefix(ctx)}{ctx.command.name} {syntax}`")

        if ctx.command.aliases:
            embed.add_field(name="Aliases", value="\n".join(f"`{i}`" for i in ctx.command.aliases), inline=False)

        embed.add_field(name="Symbol explanation",
                        value="`<...>` - Required argument\n`[...]` - Optional argument\n`(...)` - explanation\n`|` - or",
                        inline=False)

    elif isinstance(error, MemberNotFound):
        embed.description = "Member `" + error.argument + "` not found"
    elif isinstance(error, MissingPermissions):

        permissions = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(permissions) > 2:
            fmt = '{} and `{}`'.format(", ".join(f"`{i}`" for i in permissions[:-1]), permissions[-1])
        else:
            fmt = ' and '.join(f"`{i}`" for i in permissions)

        name = "s" if len(permissions) > 1 else ""
        embed.add_field(name="Missing Permissions",
                        value=f"You do not have the required permission to execute this command\nRequired permission{name}:\n" + fmt)
    else:
        embed.add_field(name="Unknown error", value=str(error), inline=False)
        embed.add_field(name="Debug Information", value=str(type(error)), inline=False)

    await ctx.send(embed=embed)


logger.init()

add_cogs(bot, Moderation, Settings, Events)
bot.run(database.get_token())
