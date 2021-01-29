from datetime import datetime
from typing import Optional

from discord import TextChannel
from discord.embeds import Embed
from discord.ext.commands import Cog, Context, group, has_permissions

from colors import Colors
from log import update_log_channel, get_log_channel, log
from translation import update_user_language, get_user_language, get_languages, get_language
from util import update_prefix, can_run_command


class Settings(Cog):
    def __init__(self, bot):
        self.bot = bot

    @group(name="settings", aliases=["config"])
    async def settings(self, ctx: Context):
        lang = get_user_language(ctx.author.id)
        embed = Embed(color=Colors.default, timestamp=datetime.now())
        embed.add_field(name="__" + lang.settings_private_settings + "__", value="** **", inline=False)
        embed.add_field(name=lang.settings_language_language, value=f"`{lang.name}`")

        if (log := await can_run_command(ctx, "settings log")) | (
                pref := await can_run_command(ctx, "settings prefix")):
            embed.add_field(name="** **", value="** **", inline=False)
            embed.add_field(name="__" + lang.settings_server_settings + "__", value="** **", inline=False)

        if log:
            embed.add_field(name=lang.settings_log_log_channel,
                            value=ctx.guild.get_channel(channel_id=get_log_channel(ctx)).mention)

        prefixes = await ctx.bot.get_prefix(ctx.message)
        if pref:
            embed.add_field(name=lang.settings_prefix_prefix, value=f"`{prefixes[0]}`")

        embed.add_field(name="** **", value="** **", inline=False)
        embed.add_field(name="__" + lang.settings_change_settings + "__",
                        value=f"`{prefixes[0]}settings <{lang.settings_change_settings_setting}> [{lang.settings_change_settings_value}]`",
                        inline=False)

        await ctx.send(embed=embed)

    @settings.command()
    @has_permissions(administrator=True)
    async def log(self, ctx: Context, channel: Optional[TextChannel] = None):
        lang = get_user_language(ctx.author.id)
        if channel:
            update_log_channel(channel)
            embed = Embed(color=Colors.log_channel, timestamp=datetime.now())
            embed.add_field(name=lang.settings_log_new_log_channel, value=channel.mention)
            embed.add_field(name=lang.changed_by, value=ctx.author.mention)
            embed.set_footer(text=lang.channel_id + ": " + str(channel.id))
            await ctx.send(embed=embed)
            await log(ctx, embed=embed)
            return

        ch = ctx.guild.get_channel(channel_id=get_log_channel(ctx))
        embed = Embed(color=Colors.log_channel, timestamp=datetime.now())
        embed.add_field(name=lang.settings_log_current_log_channel, value=ch.mention if ch else f"`{lang.none}`")
        await ctx.send(embed=embed)

    @settings.command()
    @has_permissions(administrator=True)
    async def prefix(self, ctx: Context, prefix: Optional[str] = ""):
        lang = get_user_language(ctx.author.id)
        if prefix == "":
            embed = Embed(color=Colors.default, timestamp=datetime.now())
            prefixes = await ctx.bot.get_prefix(ctx.message)
            embed.add_field(name=lang.settings_prefix_current_prefix, value=f"`{prefixes[0]}`", inline=False)
            embed.add_field(name=lang.settings_prefix_change_prefix,
                            value=f"`{prefixes[0]}settings prefix <{lang.settings_prefix_new_prefix}>`", inline=False)
            await ctx.send(embed=embed)
        else:
            new_prefix = update_prefix(ctx.guild.id, prefix)
            embed = Embed(color=Colors.default, timestamp=datetime.now())
            embed.description = lang.f_settings_prefix_changed_new_prefix(f"`{new_prefix}`")
            embed.add_field(name=lang.changed_by, value=ctx.author.mention)
            embed.set_footer(text=lang.member_id + ": " + str(ctx.author.id))
            await log(ctx, embed=embed)
            await ctx.send(embed=embed)

    @settings.command(aliases=["lang"])
    async def language(self, ctx: Context, language_abbreviation: Optional[str] = ""):
        if language_abbreviation == "":
            userlang = get_user_language(ctx.author.id)
            embed = Embed(color=Colors.default, timestamp=datetime.now())

            embed.add_field(name=userlang.settings_language_current_language,
                            value=f"`{userlang.abbreviation} ({userlang.name})`", inline=False)

            embed.add_field(name=userlang.settings_language_all_languages, value="** **", inline=False)
            for lang in get_languages().keys():
                embed.add_field(name=get_language(lang).name,
                                value=f"**{userlang.settings_language_abbreviation}**\n`{lang}`")

            prefixes = await ctx.bot.get_prefix(ctx.message)
            embed.add_field(name=userlang.settings_language_change_language,
                            value=f"`{prefixes[0]}settings language <{userlang.settings_language_new_language}>`",
                            inline=False)

            await ctx.send(embed=embed)
        else:
            if language_abbreviation not in get_languages().keys():
                lang = get_user_language(ctx.author.id)

                embed = Embed(color=Colors.error, timestamp=datetime.now())
                embed.description = lang.f_settings_language_language_does_not_exists(f"`{language_abbreviation}`")

                prefixes = await ctx.bot.get_prefix(ctx.message)
                embed.description += "\n" + lang.f_settings_language_list_all_languages(
                    f"`{prefixes[0]}settings language`")
                await ctx.send(embed=embed)
                return

            lang = update_user_language(ctx.author.id, language_abbreviation)
            embed = Embed(color=Colors.default, timestamp=datetime.now())
            embed.description = lang.f_settings_language_changed_language(f"`{lang.abbreviation} ({lang.name})`")
            await ctx.send(embed=embed)


def setup(bot):
    bot.addCog(Settings(bot))
