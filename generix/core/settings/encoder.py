"""

"""
import json
import enum


class SettingsEncoder(json.JSONEncoder):
    def default(self, o):
        return self._normalize_dict(o.__settings__)

    def _normalize_dict(self, settings):
        normalized_settings = {}
        for key, option in settings.items():
            if isinstance(option, enum.Enum):
                normalized_settings[key] = option.value
            elif isinstance(option, dict):
                normalized_settings[key] = self._normalize_dict(option)
            elif isinstance(option, list):
                normalized_settings[key] = self._normalize_list(option)
            else:
                normalized_settings[key] = option
        return normalized_settings

    def _normalize_list(self, settings):
        normalized_settings = []
        for option in settings:
            if isinstance(option, enum.Enum):
                normalized_settings.append(option.value)
            elif isinstance(option, dict):
                normalized_settings.append(self._normalize_dict(option))
            elif isinstance(option, list):
                normalized_settings.append(self._normalize_list(option))
            else:
                normalized_settings.append(option)
        return normalized_settings
