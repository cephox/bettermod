from discord.ext.commands import AutoShardedBot

from cogs.event import Events
from util import start_bot, add_cogs

bot = AutoShardedBot("--")
add_cogs(bot, Events)
start_bot(bot)
