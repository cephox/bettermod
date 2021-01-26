from datetime import datetime

from discord.colour import Color
from discord.embeds import Embed
from discord.ext.commands import Cog, Bot
from discord.message import Message
from discord.raw_models import RawMessageDeleteEvent
from discord.utils import get

from logger import log


class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    async def on_message_delete(self, message: Message):
        if message.content:
            embed = Embed(title="Message deleted", color=Color.orange(), timestamp=datetime.now())
            embed.add_field(name="Content", value=message.content, inline=False)
            embed.add_field(name="Channel", value=message.channel.mention)
            embed.set_author(name=message.author.name + "#" + message.author.discriminator,
                             icon_url=message.author.avatar_url)
            if time := message.edited_at: embed.add_field(name="last edit", value=time)
            embed.set_footer(text=f"Author: {message.author.id} | Message ID: {message.id}")

            await log(message.guild, embed=embed)

    @Cog.listener()
    async def on_raw_message_delete(self, payload: RawMessageDeleteEvent):
        if payload.cached_message:
            await self.on_message_delete(payload.cached_message)
            return

        guild = self.bot.get_guild(payload.guild_id)

        embed = Embed(title="Uncached Message deleted", color=Color.orange(), timestamp=datetime.now())
        channel = get(guild.channels, id=payload.channel_id)
        embed.add_field(name="Channel", value=channel.mention)
        embed.add_field(name="Message ID", value=payload.message_id)
        await log(guild, embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
