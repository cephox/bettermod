from discord.ext.commands import Context, check, MissingPermissions
from discord.member import Member
from discord.role import Role

from database import database

permissions = {
    "moderator": 0b1
}


def has_own_permissions(**perms):
    def wrapper(ctx: Context):
        user_perms = get_user_role_permissions(ctx.author)
        missing = [i for i in perms if not has_own_permission(i, user_perms)]

        if missing:
            raise MissingPermissions(missing)

        return True

    return check(wrapper)


def get_user_role_permissions(member: Member):
    perms = get_user_permissions(member)
    for role in member.roles:
        perms |= get_role_permissions(role)
    return perms


def list_user_permissions(member: Member):
    perms = get_user_permissions(member)
    return [p for p in permissions if perms & permissions[p]]


def list_role_permissions(role: Role):
    perms = get_role_permissions(role)
    return [p for p in permissions if perms & permissions[p]]


def get_user_permissions(member: Member):
    guild = database.get_guild(member.guild.id)
    try:
        return guild["user_permission_" + str(member.id)]
    except KeyError:
        database.update_guild(member.guild.id, {"user_permission_" + str(member.id): 0})
        return get_user_permissions(member)


def get_role_permissions(role: Role):
    guild = database.get_guild(role.guild.id)
    try:
        return guild["role_permission_" + str(role.id)]
    except KeyError:
        database.update_guild(role.guild.id, {"role_permission_" + str(role.id): 0})
        return get_role_permissions(role)


def update_user_permission(member: Member, permission, enabled: bool):
    perms = get_user_permissions(member)
    if enabled and not has_own_permission(permission, perms):
        perms = perms ^ permissions[permission]
    elif not enabled and has_own_permission(permission, perms):
        perms = perms ^ permissions[permission]
    database.update_guild(member.guild.id, {"user_permission_" + str(member.id): perms})


def update_role_permission(role: Role, permission, enabled: bool):
    perms = get_role_permissions(role)
    if enabled and not has_own_permission(permission, perms):
        perms = perms ^ permissions[permission]
    elif not enabled and has_own_permission(permission, perms):
        perms = perms ^ permissions[permission]
    database.update_guild(role.guild.id, {"role_permission_" + str(role.id): perms})


def has_own_permission(permission, current_perms):
    val = permissions[permission]
    res = val & current_perms
    return res >> val - 1 == 1
