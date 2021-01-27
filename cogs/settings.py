from datetime import datetime

from discord.channel import TextChannel
from discord.embeds import Embed
from discord.ext.commands import Cog, Bot, Context, group, has_permissions
from discord.utils import get

from colours import Colours
from database import database
from logger import log


class Settings(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @group(name="settings", aliases=["config"])
    @has_permissions(administrator=True)
    async def settings(self, ctx: Context):
        pass

    @settings.command()
    async def log(self, ctx: Context, channel: TextChannel):
        """
        Changes the channel to the preferred log channel.
        <textchannel>
        """
        embed: Embed = Embed(title="Changed log channel", color=Colours.default, timestamp=datetime.now())

        try:
            old_channel_id = database.get_guild(ctx.guild.id)["log_channel"]
            old_channel: TextChannel = get(ctx.guild.channels, id=old_channel_id)
            embed.add_field(name="Old channel", value=old_channel.mention)
        except KeyError:
            pass

        database.update_guild(ctx.guild.id, {"log_channel": channel.id})

        embed.add_field(name="New channel", value=channel.mention)
        embed.set_footer(text="Channel changed by " + ctx.author.name + "#" + ctx.author.discriminator)

        await ctx.send(embed=embed)
        await log(ctx.guild, embed=embed)


def setup(bot):
    bot.add_cog(Settings(bot))
