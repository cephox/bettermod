from database import database
from sys import argv


def check_for_token():
    if len(argv) == 2:
        if argv[1] == "reset":
            database.reset()
            print("The bot has been reset successfully")
            exit(0)

        database.set_token(argv[1])
        print("The bots token has been set")
        print("Starting ...")
        print()

    if database.get_token() is None:
        print("No token has been provided so far")
        print("To start the bot, pass the token as the first argument")
        exit(0)


def add_cogs(bot, *cogs):
    for cog_c in cogs:
        if cog_c is None:
            continue
        cog = cog_c(bot)
        bot.add_cog(cog)
