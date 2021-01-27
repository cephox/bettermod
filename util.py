from sys import argv

from database import database


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
