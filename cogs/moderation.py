from language import get_user_language, Language

from discord.ext.commands import Cog, Bot, command, Context
from discord.member import Member
from discord.embeds import Embed
from discord.colour import Color

from datetime import datetime


class Moderation(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @command()
    async def info(self, ctx: Context, member: Member):
        lang: Language = get_user_language(ctx.author.id)

        embed: Embed = Embed(title=lang.f_info_information_about(member.name),
                             color=member.color if member.color != Color(0x000) else Color(0x1bb6d1),
                             timestamp=datetime.now())

        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(name=lang.info_display_name, value=f"{member.display_name}")
        embed.add_field(name=lang.info_roles,
                        value=" ".join(r.mention for r in member.roles[::-1] if r.name != "@everyone"))
        embed.add_field(name=lang.info_mention, value=member.mention)
        embed.add_field(name=lang.info_id, value=f"{member.id}")
        embed.add_field(name=lang.info_bot, value="Yes" if member.bot else "No")
        embed.add_field(name=lang.info_administrator, value="Yes" if member.guild_permissions.administrator else "No")
        embed.add_field(name=lang.info_created, value=f"{member.created_at}")
        embed.add_field(name=lang.info_joined, value=f"{member.joined_at}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
