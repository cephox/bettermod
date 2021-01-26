from util import can_interact

from discord.ext.commands import Cog, Bot, command, Context, has_permissions
from discord.member import Member
from discord.embeds import Embed
from discord.colour import Color

from datetime import datetime

from typing import Optional


class Moderation(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx: Context, member: Member, *, reason: Optional[str] = ""):
        """
        Kicks a member
        <member> [reason]
        """

        if not can_interact(ctx.author, member):
            error: Embed = Embed(title="Missing Permissions",
                                 description="You cannot kick " + member.mention, color=Color(0xff0000),
                                 timestamp=datetime.now())
            await ctx.send(embed=error)
            return

        if not can_interact(ctx.me, member):
            error: Embed = Embed(title="Missing Permissions",
                                 description="I cannot kick " + member.mention, color=Color(0xff0000),
                                 timestamp=datetime.now())
            await ctx.send(embed=error)
            return

        embed: Embed = Embed(title="Kicked " + str(member), color=Color(0xc9b200), timestamp=datetime.now())
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="kicked by", value=ctx.author.display_name, inline=False)
        await ctx.send(embed=embed)

        private: Embed = Embed(title="You have been kicked from " + ctx.guild.name, color=Color(0xc9b200),
                               timestamp=datetime.now())
        if reason:
            private.add_field(name="Reason", value=reason, inline=False)
        private.add_field(name="kicked by", value=ctx.author.display_name, inline=False)
        await member.send(embed=private)

        await member.kick(reason=reason)

    @has_permissions(manage_messages=True)
    @command(aliases=["purge"])
    async def clear(self, ctx: Context, amount: int):
        deleted = await ctx.channel.purge(limit=amount + 1)
        message = await ctx.send(embed=Embed(description=f"Deleted {len(deleted) - 1} message(s)", color=Color.greyple()))
        await message.delete(delay=3)

    @command()
    async def info(self, ctx: Context, member: Member):
        """
        Displays information about a guild member
        <member>
        """
        embed: Embed = Embed(title=member.name,
                             color=member.color if member.color != Color(0x000) else Color(0x1bb6d1),
                             timestamp=datetime.now())

        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(name="Display name", value=f"{member.display_name}")
        embed.add_field(name="Roles",
                        value=" ".join(r.mention for r in member.roles[:0:-1]))
        embed.add_field(name="Mention", value=member.mention)
        embed.add_field(name="ID", value=f"{member.id}")
        embed.add_field(name="Bot", value=":white_check_mark:" if member.bot else ":x:")
        embed.add_field(name="Administrator",
                        value=":white_check_mark:" if member.guild_permissions.administrator else ":x:")
        embed.add_field(name="joined", value=f"{member.joined_at}")
        embed.add_field(name="created", value=f"{member.created_at}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
