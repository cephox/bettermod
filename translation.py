import copy
import os

import yaml

from database import database


class Language:
    def __init__(self, abbreviation):
        self.abbreviation = abbreviation
        self._translations = yaml.safe_load(open(f"translation/{abbreviation}.yml"))
        self.name = self._translations["name"]

    def reload(self):
        self._translations = yaml.safe_load(open(f"translation/{self.abbreviation}.yml"))

    def __getattr__(self, item):
        if item == "_translations":
            return self._translations
        if item.startswith("f_"):
            return self._translations[item[2:]].format
        return copy.deepcopy(self._translations[item])


_languages = dict()


def get_language(abbr="en"):
    return _languages[abbr]


def get_languages():
    return _languages


def get_user_language(uid):
    return get_language(database.get_user(uid)["language"])


def update_user_language(uid, abbr):
    database.update_user(uid, {"language": abbr})
    return get_user_language(uid)


def load():
    for file in os.listdir("./translation"):
        abbr = file[::-1].split(".", 1)[::-1][0][::-1]
        _languages[abbr] = Language(abbr)
