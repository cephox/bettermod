from database import database

from discord.ext.commands import Context, check


def is_owner():
    async def predicate(ctx: Context):
        return str(ctx.author.id) == str(database.get_setting("owner_id"))

    return check(predicate)
