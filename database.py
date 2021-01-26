from pymongo import MongoClient

user_defaults = dict()
guild_defaults = dict()


class Database:
    def __init__(self, port: str = "27017"):
        self.client = MongoClient("mongodb://localhost:" + port)
        self.db = self.client["bettermod"]
        self.settings = self.db["settings"]
        self.users = self.db["users"]
        self.guilds = self.db["guilds"]

    def reset(self):
        self.client.drop_database("bettermod")

    def update_guild(self, guild_id, data: dict):
        self.guilds.update_one({"guild_id": guild_id}, {"$set": data})

    def get_guild(self, guild_id):

        guild = self.guilds.find_one({"guild_id": guild_id})
        if guild:
            return guild
        guild_defaults["guild_id"] = guild_id

        self.guilds.insert_one(guild_defaults)
        return self.get_guild(guild_id)

    def update_user(self, user_id, data: dict):
        self.users.update_one({"user_id": user_id}, {"$set": data})

    def get_user(self, user_id):
        user = self.users.find_one({"user_id": user_id})
        if user:
            return user
        user_defaults["user_id"] = user_id
        self.users.insert_one(user_defaults)
        return self.get_user(user_id)

    def set_setting(self, name, value):
        self.settings.delete_one({"name": name})
        self.settings.insert_one({"name": name, "value": value})

    def get_setting(self, name):
        res = self.settings.find_one({"name": name})
        if res is None:
            return None
        return res["value"]

    def get_token(self):
        return self.get_setting("token")

    def set_token(self, token: str):
        self.set_setting("token", token)


database: Database = Database()
