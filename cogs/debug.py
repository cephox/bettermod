import os

from discord.embeds import Embed
from discord.ext.commands import Bot, Cog, Context, command, is_owner


class Debugging(Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @command(name="eval")
    @is_owner()
    async def _eval(self, ctx: Context, *, cmd: str):
        await ctx.send(eval(cmd))

    @command(name="load")
    @is_owner()
    async def _load(self, ctx: Context, *, module: str):
        embed = Embed(title="Loading " + module, description="", color=0x808080, timestamp=ctx.message.created_at)

        try:
            self.bot.load_extension(f"cogs.{module}")
            embed.description += f"Loaded `{module}.py`\n"
        except Exception:
            embed.description += f"Failed to load `{module}`\n"

        await ctx.send(embed=embed)

    @command(name="unload")
    @is_owner()
    async def _unload(self, ctx: Context, *, module: str):
        embed = Embed(title="Unloading " + module, description="", color=0x808080, timestamp=ctx.message.created_at)

        try:
            self.bot.unload_extension(f"cogs.{module}")
            embed.description += f"Unloaded `{module}.py`\n"
        except Exception:
            embed.description += f"Failed to unload `{module}`\n"

        await ctx.send(embed=embed)

    @command(name="reload")
    @is_owner()
    async def _reload(self, ctx: Context):
        embed = Embed(title="Reloading all cogs", description="", color=0x808080, timestamp=ctx.message.created_at)

        for ext in set([i[5:] + ".py" for i in self.bot.extensions] + os.listdir("cogs")):
            if ext.endswith(".py") and not ext.startswith("_"):
                try:

                    unloaded = False
                    loaded = False

                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        unloaded = True
                    except Exception:
                        pass
                    try:
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        loaded = True
                    except Exception:
                        pass

                    if unloaded and loaded:
                        embed.description += f"Reloaded `{ext}`\n"
                    elif unloaded:
                        embed.description += f"Unloaded `{ext}`\n"
                    elif loaded:
                        embed.description += f"Loaded `{ext}`\n"

                except Exception:
                    embed.description += f"Failed to reload `{ext}`\n"

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Debugging(bot))
