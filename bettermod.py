#!/bin/python
from discord.ext.commands import AutoShardedBot

import translation
from cogs.event import Events
from cogs.settings import Settings
from util import start_bot, add_cogs, get_prefix

bot = AutoShardedBot(get_prefix)
translation.load()
add_cogs(bot, Events, Settings)
start_bot(bot)
