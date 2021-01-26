from discord.member import Member

from database import database
from sys import argv


def can_interact(member: Member, target: Member):
    if member.guild != target.guild:
        return False

    if member.guild.owner == member:
        return True

    if target.guild.owner == target:
        return False

    return member.top_role.position > target.top_role.position


def check_for_token():
    if len(argv) == 2:
        if argv[1] == "reset":
            database.reset()
            print("The bot has been reset")
            exit(0)

    if database.get_token() is None:
        print("No token has been provided so far")
        print("")
        database.set_token(input("Please enter your discord bot token: "))
        print("")
        print("The bot is now starting\n")


def add_cogs(bot, *cogs):
    for cog_c in cogs:
        if cog_c is None:
            continue
        cog = cog_c(bot)
        bot.add_cog(cog)
