#!/bin/python
from database import database
from util import check_for_token

from discord.ext.commands import AutoShardedBot

check_for_token()

bot: AutoShardedBot = AutoShardedBot("--")

bot.start(database.get_token())
