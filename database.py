from pymongo import MongoClient


class Database:
    def __init__(self, port: str = "27017"):
        self.client = MongoClient("mongodb://localhost:" + port)
        self.db = self.client["bettermod"]
        self.settings = self.db["settings"]
        self.users = self.db["users"]
        self.guilds = self.db["guilds"]

    def reset(self):
        self.client.drop_database("bettermod")

    def get_token(self):
        token = self.settings.find_one()
        if token is None:
            return None
        return token["token"]

    def set_token(self, token: str):
        self.settings.remove(0)
        self.settings.insert_one({"_id": 0, "token": token})


database: Database = Database()
