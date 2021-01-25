from database import database, user_defaults

import yaml
import copy


class Language:
    def __init__(self, name, abbreviation):
        self.abbreviation = abbreviation
        self.name = name
        self._translations = yaml.safe_load(open(f"assets/lang/{abbreviation}.yml"))

    def reload(self):
        self._translations = yaml.safe_load(open(f"assets/lang/{self.abbreviation}.yml"))

    def __getattr__(self, item):
        if item == "_translations":
            return self._translations
        if item.startswith("f_"):
            return self._translations[item[2:]].format

        if item == "abbreviation":
            return self.abbreviation

        if item == "name":
            return self.name

        return copy.deepcopy(self._translations[item])


_languages = {}


def add_languages(*languages: Language):
    for l in languages:
        _languages[l.abbreviation] = l


def get_language(abbr="en"):
    return _languages[abbr]


def get_languages():
    return _languages


def get_user_language(uid):
    return get_language(database.get_user(uid)["language"])


def init():
    user_defaults["language"] = "en"
    add_languages(Language("English", "en"), Language("German", "de"))
