"""

"""
import json
import copy

from generix.core.settings.settings import DEFAULT_SETTINGS, SETTINGS_FILE_PATH, LOAD_SETTINGS
from generix.core.settings.encoder import SettingsEncoder


class SettingsRegistry:
    def __init__(self, path, default_settings):
        """
        Constructs SettingsRegistry instance.
        :param path: path to the settings file.
        :param default_settings: default settings dictionary.
        """
        self._path = path
        self.__original = copy.deepcopy(default_settings)
        self._settings = self.delete_ignored_items(default_settings)

    def load(self):
        """
        Loads last saved data from settings.json.
        :return: None.
        """
        with open(self._path, mode='r', encoding='utf-8') as f:
            self._settings = json.load(f)

    def save(self):
        """
        Saves current settings to the file, rewriting it.
        :return: None.
        """
        with open(self._path, mode='w', encoding='utf-8') as f:
            json.dump(self._settings, f, cls=SettingsEncoder)

    def create(self, key, value):
        """
        Adds new item to the storage.
        :param key: key.
        :param value: value.
        :return: None.
        """
        self._settings[key] = value

    def find(self, key):
        """
        Searches for item by name and returns it.
        :param key: genome name.
        :return: dict value of the key.
        """
        return SettingsRegistry.search(self._settings, key)

    def find_option_by_key(self, key, option):
        """
        Searches for specific option and returns it.
        :param key: key.
        :param option: inner dict key.
        :return: option value.
        """
        return SettingsRegistry.search(self.find(key), option)

    def find_option_by_attr(self, attr_key, attr_value, option):
        """
        Searches for specific option by attribute with value.
        :param attr_key: key.
        :param attr_value: value.
        :param option: inner dict key.
        :return: option value.
        """
        for k, v in self._settings.items():
            if v[attr_key] == attr_value:
                return SettingsRegistry.search(v, option)
        return None

    def delete_ignored_items(self, settings, depth=0):
        """
        Deletes dicts which contain 'ignore': True attribute recursively.
        :param settings: dictionary with settings.
        :param depth: depth of recursion.
        :return: updated dictionary with settings.
        """
        for k, v in copy.copy(settings).items():
            if k == 'ignore' and v is True:
                if depth == 0:
                    return {}
                else:
                    return True
            if isinstance(v, dict):
                if self.delete_ignored_items(v, depth + 1):
                    del settings[k]
        if depth == 0:
            return settings
        else:
            return False

    @staticmethod
    def search(dictionary, option):
        """
        Recursively searches option in dict.
        :param dictionary: dictionary object.
        :param option: key to search to.
        :return: value of option.
        """
        for k, v in dictionary.items():
            if k == option:
                return v
            if isinstance(v, dict):
                item = SettingsRegistry.search(v, option)
                if item is None:
                    continue
                return item
        return None


settings_reg = SettingsRegistry(SETTINGS_FILE_PATH, DEFAULT_SETTINGS)

# Reads only if file existed before program execution
if LOAD_SETTINGS:
    settings_reg.load()
