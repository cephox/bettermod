from sys import argv

from discord.message import Message

from database import database, guild_defaults


def start_bot(bot):
    if len(argv) == 2:
        if argv[1] == "reset":
            database.reset()
            print("The bot has been reset")
            exit(0)

    if database.get_token() is None:
        print("No token has been provided so far")
        database.set_token(input("Please enter your discord bot token: "))
        print()

    print("Starting...")
    bot.run(database.get_token())


def add_cogs(bot, *cogs):
    for cog_c in cogs:
        if cog_c is None:
            continue
        cog = cog_c(bot)
        bot.add_cog(cog)


def update_prefix(guild_id, prefix):
    database.update_guild(guild_id, {"prefix": prefix})
    return database.get_guild(guild_id)["prefix"]


def get_prefix(bot, message: Message):
    guild = database.get_guild(message.guild.id)

    try:
        p = guild["prefix"]
    except KeyError:
        database.update_guild(message.guild.id, {"prefix": guild_defaults["prefix"]})
        return get_prefix(bot, message)

    return p, f"<@!{bot.user.id}> ", f"<@{bot.user.id}> "
