from discord.ext.commands import Cog, Bot, command, Context
from discord.ext.commands.errors import MissingRequiredArgument, MemberNotFound
from discord.member import Member
from discord.embeds import Embed
from discord.colour import Color

from datetime import datetime


class Moderation(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @command()
    async def info(self, ctx: Context, member: Member):
        """
        Displays information about a guild member
        Syntax: <member>
        """
        embed: Embed = Embed(title=member.name,
                             color=member.color if member.color != Color(0x000) else Color(0x1bb6d1),
                             timestamp=datetime.now())

        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(name="Display name", value=f"{member.display_name}")
        embed.add_field(name="Roles",
                        value=" ".join(r.mention for r in member.roles[::-1] if r.name != "@everyone"))
        embed.add_field(name="Mention", value=member.mention)
        embed.add_field(name="ID", value=f"{member.id}")
        embed.add_field(name="Bot", value="✓" if member.bot else "✗")
        embed.add_field(name="Administrator",
                        value="✓" if member.guild_permissions.administrator else "✗")
        embed.add_field(name="joined", value=f"{member.joined_at}")
        embed.add_field(name="created", value=f"{member.created_at}")
        await ctx.send(embed=embed)

    @info.error
    async def info_error(self, ctx: Context, error):
        embed = Embed(color=Color(0xff0000))

        if isinstance(error, MissingRequiredArgument):
            embed.add_field(name="Syntax",
                            value=f"`{await ctx.bot.get_prefix(ctx)}info <member (id|mention)>`")
        elif isinstance(error, MemberNotFound):
            embed.description = "Member `" + error.argument + "` not found"
        else:
            embed.add_field(name="Unknown error", value=error)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
