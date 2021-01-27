import copy

import yaml

from database import database


class Language:
    def __init__(self, name, abbreviation):
        self.abbreviation = abbreviation
        self.name = name
        self._translation = yaml.safe_load(open(f"translation/{abbreviation}.yml"))

    def reload(self):
        self._translation = yaml.safe_load(open(f"translation/{self.abbreviation}.yml"))

    def __getattr__(self, item):
        if item == "_translations":
            return self._translations
        if item.startswith("f_"):
            return self._translations[item[2:]].format
        return copy.deepcopy(self._translations[item])


_languages = {
    "en": Language("English", "en"),
    "de": Language("Deutsch", "de")
}


def get_language(abbr="en"):
    return _languages[abbr]


def get_languages():
    return _languages


def get_user_language(uid):
    return get_language(database.get_user(uid)["language"])
