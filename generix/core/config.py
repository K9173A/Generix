"""
A module for game parameters.
"""
import json
import configparser

from generix.core.file import File


class Config(File):
    """
    Config - stores all application settings.
    """
    def __init__(self, path, mode, encoding='utf-8'):
        """
        Constructs Config instance.
        :param path: path to the config.ini.
        """
        super(Config, self).__init__(path, mode, encoding, False)
        self._config = configparser.ConfigParser()
        if self.exists():
            self._config.read(path, encoding)
        else:
            self.create()
            self._config.add_section('SETTINGS')
            self.drop_to_default()
            self.rewrite()

    def drop_to_default(self):
        """
        Writes 'SETTINGS' section of the autoexec.ini.
        :return: None.
        """
        self._config["SETTINGS"] = {
            "window_width": 900,
            "window_height": 800,
            "board_width": 20,
            "board_height": 20,
            "cell_width": 40,
            "cell_height": 40,
            "genome_size": 16,
        }

    def get_option(self, section, option):
        """
        Gets value of a specific option.
        :param section: section name.
        :param option: option to search to.
        :return: option value.
        """
        return self._config.get(section, option)

    def set_option(self, section, option, value):
        """
        Sets new value to a specific option.
        :param section: section name.
        :param option: option name.
        :param value: new value.
        :return: None.
        """
        self._config.set(section, option, value)

    def set_options(self, section, **options):
        """
        Sets block of values in a specific section.
        :param section: section name
        :param options: options dictionary.
        :return: None.
        """
        for k, v in options.items():
            if type(k) != str:
                k = json.dumps(k)
            if type(v) != str:
                v = json.dumps(v)
            self.set_option(section, k, v)

    def get_section(self, section):
        """
        Gets entire section.
        :param section: section name.
        :return: dict of section attributes.
        """
        return {k: json.loads(v.replace("\'", "\"")) for k, v in self._config.items(section)}

    def rewrite(self):
        """
        Rewrites config file.
        :return: None.
        """
        with open(self._path, 'w') as f:
            self._config.write(f)
