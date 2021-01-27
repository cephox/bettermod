from typing import Optional

from discord.embeds import Embed
from discord.ext.commands import Cog, Context, group, has_permissions

from colors import Colors
from translation import update_user_language, get_user_language, get_languages, get_language
from util import update_prefix


class Settings(Cog):
    def __init__(self, bot):
        self.bot = bot

    @group(name="settings", aliases=["config"])
    async def settings(self, ctx: Context):
        pass

    @settings.command()
    @has_permissions()
    async def prefix(self, ctx: Context, prefix: Optional[str] = ""):
        lang = get_user_language(ctx.author.id)
        if prefix == "":
            embed = Embed(color=Colors.default)
            prefixes = await ctx.bot.get_prefix(ctx.message)
            embed.add_field(name=lang.settings_prefix_current_prefix, value=f"`{prefixes[0]}`", inline=False)
            embed.add_field(name=lang.settings_prefix_change_prefix,
                            value=f"`{prefixes[0]}settings prefix <{lang.settings_prefix_new_prefix}>`", inline=False)
            await ctx.send(embed=embed)
        else:
            new_prefix = update_prefix(ctx.guild.id, prefix)
            embed = Embed(color=Colors.default)
            embed.description = lang.f_settings_prefix_changed_new_prefix(f"`{new_prefix}`")
            await ctx.send(embed=embed)

    @settings.command(aliases=["lang"])
    async def language(self, ctx: Context, language_abbreviation: Optional[str] = ""):
        if language_abbreviation == "":
            userlang = get_user_language(ctx.author.id)
            embed = Embed(color=Colors.default)

            embed.add_field(name="Current language", value=f"`{userlang.abbreviation} ({userlang.name})`", inline=False)

            embed.add_field(name=userlang.settings_language_all_languages, value="** **", inline=False)
            for lang in get_languages().keys():
                embed.add_field(name=get_language(lang).name,
                                value=f"**{userlang.settings_language_abbreviation}**\n`{lang}`")

            await ctx.send(embed=embed)
        else:
            if language_abbreviation not in get_languages().keys():
                lang = get_user_language(ctx.author.id)

                embed = Embed(color=Colors.error)
                embed.description = lang.f_settings_language_language_does_not_exists(f"`{language_abbreviation}`")
                embed.description += "\n" + lang.f_settings_language_list_all_languages(
                    f"`{await ctx.bot.get_prefix(ctx.message)}settings language`")
                await ctx.send(embed=embed)
                return

            lang = update_user_language(ctx.author.id, language_abbreviation)
            embed = Embed(color=Colors.default)
            embed.description = lang.f_settings_language_changed_language(f"`{lang.abbreviation} ({lang.name})`")
            await ctx.send(embed=embed)


def setup(bot):
    bot.addCog(Settings(bot))
