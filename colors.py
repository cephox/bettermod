from discord.colour import Color
from discord.member import Member


class Colors:
    red = Color.red()
    orange = Color.orange()

    default = Color(0x006e7a)

    error = Color(0xff0000)
    warning = Color(0xffd500)

    @staticmethod
    def member(member: Member):
        return member.color
