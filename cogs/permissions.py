from datetime import datetime

from discord.embeds import Embed
from discord.ext.commands import Cog, Context, group, has_permissions
from discord.member import Member

from colors import Colors
from permission import update_user_permission, list_user_permission, get_user_permissions, has_own_permission
from translation import get_user_language


class Permissions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @group()
    @has_permissions(administrator=True)
    async def permissions(self, ctx: Context):
        pass

    @permissions.command()
    async def member(self, ctx: Context, member: Member, permission: str, enabled: int):
        lang = get_user_language(ctx.author.id)

        before = lang.yes if has_own_permission(permission, get_user_permissions(member)) else lang.no

        update_user_permission(member, permission, enabled > 0)

        embed = Embed(color=Colors.permission, timestamp=datetime.now())
        embed.add_field(name=lang.f_permissions_permission_set_for(str(member)),
                        value="`" + permission.title().replace("_",
                                                               " ") + "` » `" + (
                                  lang.yes if enabled > 0 else lang.no) + "`",
                        inline=False)
        embed.add_field(name=lang.permissions_permission_before, value=f"`{before}`", inline=False)
        embed.add_field(name=lang.permissions_permission_set_by, value=ctx.author.mention, inline=False)
        embed.add_field(name=lang.permissions_permission_total,
                        value="\n".join([f"`{i.title().replace('_', ' ')}`" for i in
                                         list_user_permission(member)]) if list_user_permission(member) else lang.none)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=lang.member_id + str(member.id))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Permissions(bot))
