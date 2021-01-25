#!/bin/python
from database import database
from util import check_for_token, add_cogs

from discord.ext.commands import AutoShardedBot

from cogs.moderation import Moderation
from cogs.debug import Debugging

check_for_token()

bot: AutoShardedBot = AutoShardedBot("--")


@bot.event
async def on_ready():
    print("\n" + bot.user.name + " is now online.\n")


add_cogs(bot, Debugging, Moderation)
bot.run(database.get_token())
