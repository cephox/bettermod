# bettermod
a better discord moderation bot

## Invitation
bettermod is a free moderation discord bot. To invite him, click [here](https://discord.com/api/oauth2/authorize?client_id=796332608296058940&permissions=8&scope=bot).
### Permissions
The Bot needs to have access to all guild members. When you invite him, a new Role is created with the name `BetterMod`. This Role needs to have Administrator Permissions in order to access all of bettermods features.

In order to manage members that have a higher role than the bot, the bot need to have a role above all members you want to mange with this bot.
Simply drag the `BetterMod` role above every other one.

## Languages
The Bot currently supports german and english

## Commands
### Command prefix
The default command prefix is `--`.
To change it, run `--settings prefix <new prefix>`. Be aware that you need to have administrator rights on the server.
### Command list
To get a list of all commands with help, run the `help` command (not implemented yet)


## Self-installation
### Start
```bash
./bettermod.py
```
### Reset
```bash
./bettermod.py reset
```

## Requirements
- Python >= 3.9
- MondoDB >= 4.4.3
