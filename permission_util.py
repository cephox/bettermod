from discord.member import Member


def can_interact(member: Member, target: Member):
    if member.guild != target.guild:
        return False

    if member.guild.owner == member:
        return True

    if target.guild.owner == target:
        return False

    return member.top_role.position > target.top_role.position
