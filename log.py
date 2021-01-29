from discord.channel import TextChannel
from discord.ext.commands import Context
from discord.utils import get

from database import database


def get_log_channel(ctx: Context):
    try:
        return int(database.get_guild(ctx.guild.id)["log_channel"])
    except KeyError:
        database.update_guild(ctx.guild.id, {"log_channel": "0"})
        return get_log_channel(ctx)


def update_log_channel(channel: TextChannel):
    database.update_guild(channel.guild.id, {"log_channel": channel.id})


async def log(ctx: Context, *, content="", embed=None):
    if (ch_id := get_log_channel(ctx)) == 0:
        return

    channel: TextChannel = get(ctx.guild.channels, id=ch_id)
    await channel.send(content=content, embed=embed)
