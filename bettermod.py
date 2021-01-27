#!/bin/python
from discord.ext.commands import AutoShardedBot

from cogs.event import Events
from cogs.settings import Settings
from util import start_bot, add_cogs

bot = AutoShardedBot("--")
add_cogs(bot, Events, Settings)
start_bot(bot)
