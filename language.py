import yaml
import copy


class Language:
    def __init__(self, name, abbreviation):
        self.abbreviation = abbreviation
        self.name = name
        self._translation = yaml.safe_load(open(f"assets/lang/{abbreviation}.yml"))

    def reload(self):
        self._translation = yaml.safe_load(open(f"assets/lang/{self.abbreviation}.yml"))

    def __getattr__(self, item):
        if item == "_translations":
            return self._translations
        if item.startswith("f_"):
            return self._translations[item[2:]].format
        return copy.deepcopy(self._translations[item])


_languages = {}


def _add_languages(*languages: Language):
    for l in languages:
        _languages[l.abbreviation] = l


def get_language(abbr="en"):
    return _languages[abbr]


def get_languages():
    return _languages


_add_languages(Language("English", "en"), Language("German", "de"))
