from abc import abstractstaticmethod
from typing import List

from creationism.extension import Extension
from creationism.utils import open_json, open_yaml
import os
from pathlib import Path
SEARCH_PATHS = ['']

class ConfigurationFileExtension(Extension):
    @abstractstaticmethod
    def open(file_path):
        """[summary]

        Args:
            file_path ([type]): [description]

        Returns:
            [type]: [description]
        """

    @staticmethod
    def is_configuration_extension_path(path):
        return path.endswith(ConfigurationFileExtension.names())


@ConfigurationFileExtension.register((".yml", ".yaml"))
class YamlConfigurationFileExtension(ConfigurationFileExtension):
    @staticmethod
    def open(file_path):
        return open_yaml(file_path)


@ConfigurationFileExtension.register((".json",))
class JsonConfigurationFileExtension(ConfigurationFileExtension):
    @staticmethod
    def open(file_path):
        return open_json(file_path)


def open_config(config_path: Path, search_paths: List):
    for search_path in search_paths:
        search_config_path = os.path.join(search_path, config_path)
        try:
            return ConfigurationFileExtension.create(Path(config_path).suffix).open(search_config_path)
        except FileNotFoundError:
            pass
    else:
        raise FileNotFoundError(f"config not found: {config_path}")