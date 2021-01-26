from discord.channel import TextChannel
from discord.utils import get

from database import database, guild_defaults


async def log(guild, *, message=None, embed=None):
    try:
        channel_id = database.get_guild(guild.id)["log_channel"]
    except KeyError:
        return

    if channel_id == "0":
        return
    channel: TextChannel = get(guild.channels, id=channel_id)
    await channel.send(content=message, embed=embed)


def init():
    guild_defaults["log_channel"] = "0"
