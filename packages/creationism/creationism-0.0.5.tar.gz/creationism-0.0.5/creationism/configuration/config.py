import importlib
import operator
import os
import pathlib
import re
from abc import abstractmethod
from collections import UserDict, UserList, UserString
from functools import partial, reduce
from pathlib import Path
from typing import Any

from creationism.configuration.extensions import ConfigurationFileExtension, open_config
from creationism.mode import DEFAULT_MODE
from creationism.registration.factory import RegistrantFactory
from creationism.registration.utils import Text, chain_functions

_REPLACE_IDENTIFIER = r"\@replace=(True|true|False|false)"
_REFERENCE_START_SYMBOL = "$"
_REFERENCE_MAP_SYMBOL = ":"
_REFERENCE_ATTRIBUTE_SYMBOL = "."


from copy import deepcopy


class Config(RegistrantFactory):
    CONVERT_NAME = lambda x: chain_functions(
        x, Text.split_capitals, Text.lower, Text.split, partial(Text.get, index=-1)
    )

    @classmethod
    def create(cls, class_type: type, config_value: "Config", *args, **kwargs):
        if cls.registered(class_type):
            return super().create(
                class_type, config_value=config_value, *args, **kwargs
            )
        return ConfigObject(config_value, *args, **kwargs)

    @abstractmethod
    def merge(self, config_value: "Config") -> None:
        """Merges config"""

    @abstractmethod
    def cast(self) -> Any:
        """Casts the data in the config to its original type"""

    @abstractmethod
    def build(self):
        """[summary]"""


def _determine_replace(config1: Config, config2: Config):
    if config2.replace is not None:
        return config2.replace
    elif config1.replace is not None:
        return config1.replace
    return config2.__class__.REPLACE


class UserObject:
    def __init__(self, value):
        self.data = value


class ConfigObject(Config, UserObject):
    def __init__(self, config_value):
        super().__init__(config_value)

    def merge(self, config_value):
        self.data = config_value.data

    def cast(self):
        return self.data

    def build(self, configuration):
        return self


@Config.register((str,))
class ConfigString(Config, UserString):
    def __init__(self, config_value):
        super().__init__(config_value)

    def merge(self, config_value):
        self.data = config_value.data

    def cast(self):
        return self.data

    def build(self, configuration):
        if _REFERENCE_START_SYMBOL == self.data[0]:
            return self._get_reference(configuration)
        return self

    def _get_reference(self, configuration):
        self.data = self.data.replace("{", "").replace("}", "")
        references = self.data[1:].split(_REFERENCE_MAP_SYMBOL)
        reference = reduce(operator.getitem, references[:-1], configuration)
        attributes = references[-1].split(_REFERENCE_ATTRIBUTE_SYMBOL)
        reference = reference[attributes[0]].cast()
        for attr in attributes[1:]:
            reference = getattr(reference, attr)
        return ConfigObject(reference)


@Config.register((list,))
class ConfigList(Config, UserList):

    REPLACE = True

    def __init__(self, config_value, replace=None):
        super().__init__(config_value)
        self._replace = replace
        for idx in range(len(self)):
            self.data[idx] = Config.create(
                class_type=type(self[idx]), config_value=self.data[idx]
            )

    @property
    def replace(self):
        return self._replace

    def merge(self, config_value):
        """merge only possible by replace of extend, due to the ambiguity of list items ids"""

        if not isinstance(config_value, ConfigList):
            raise ValueError("unsupporterd merging of different config types")

        if _determine_replace(self, config_value):
            self.data = config_value.data
        else:
            self.data.extend(config_value.data)

    def cast(self):
        return [item.cast() for item in self]

    def build(self, configuration):
        self.data = [item.build(configuration) for item in self.data]
        return self


@Config.register((dict,))
class ConfigDict(Config, UserDict):
    REPLACE = False

    def __init__(self, config_value, replace=None):
        super().__init__(dict())
        self._replace = replace
        self._iterative_init(config_value=config_value)

    @property
    def replace(self):
        return self._replace

    def _iterative_init(self, config_value):
        for key in list(config_value):
            class_type = type(config_value[key])
            replace = re.search(_REPLACE_IDENTIFIER, key)
            if replace:
                key_stripped = key.replace(replace.group(0), "")
                replace = replace.group(1).lower() == "true"
                self.data[key_stripped] = Config.create(
                    class_type=class_type,
                    config_value=config_value[key],
                    replace=replace,
                )
            else:
                self.data[key] = Config.create(
                    class_type=class_type, config_value=config_value[key]
                )


    def merge(self, config_value):
        if not isinstance(config_value, ConfigDict):
            raise ValueError("unsupporterd merging of different config types")
        else:
            self._iterative_merge(config_value)

    def _iterative_merge(self, config_value):

        if _determine_replace(self, config_value):
            self.data = config_value.data
            return

        for key in list(config_value):
            if key not in self.data:
                self.data[key] = config_value[key]
            else:
                self.data[key].merge(config_value[key])

    def cast(self):
        return {key: value.cast() for key, value in self.items()}

    def build(self, configuration):
        registrar_module = self.data.pop("registrar_module", None)
        registrar_name = self.data.pop("registrar_name", None)
        registrant_module = self.data.pop("registrant_module", None)
        registrant_name = self.data.pop("registrant_name", None)

        module = self.data.pop("module", None)
        attribute = self.data.pop("attribute", None)

        for key, value in self.items():
            self.data[key] = value.build(configuration)

        if (
            registrar_module is not None
            and registrar_name is not None
            and registrant_name is not None
        ):
            return ConfigObject(
                _build_registrant_object(
                    self,
                    registrar_module,
                    registrar_name,
                    registrant_module,
                    registrant_name,
                )
            )

        if module is not None and attribute is not None:
            return ConfigObject(_build_object(self, module, attribute))

        return self


class Configuration(ConfigDict):

    PRESETS_FOLDER = pathlib.Path(__file__).absolute().parent / "presets"
    CONFIG_PATH = pathlib.Path(__file__).absolute().parent / os.path.join(
        "config", "config.yml"
    )
    SEARCH_PATHS = ("", pathlib.Path(__file__).absolute().parent)
    NAME = "configuration"

    def __init__(self, name, config_value, modes, search_paths=()):
        self._modes = modes
        self._name = name
        self._search_paths = self.__class__.SEARCH_PATHS + search_paths
        include_configs(config_value, self._search_paths)
        super().__init__(config_value=config_value)

    @classmethod
    def build(
        cls,
        user_config,
        modes,
        build_instances=True,
        build_key=None,
        presets=(),
        external_configurations=None,
        search_paths=(),
        *args,
        **kwargs,
    ):

        if isinstance(user_config, (str, Path)):
            search_paths = cls.SEARCH_PATHS + (Path(user_config).parent,) + search_paths
            user_config = open_config(user_config, search_paths=search_paths)[cls.NAME]
        else:
            search_paths = cls.SEARCH_PATHS + search_paths

        if cls.NAME in user_config:
            user_config = user_config[cls.NAME]

        include_configs(user_config, search_paths=search_paths)
        configuration = cls(*args, **kwargs)
        for preset in presets:
            preset_config = open_config(
                cls.PRESETS_FOLDER / (preset + ".yml"), search_paths
            )
            configuration.merge(preset_config)

        configuration.merge(user_config)
        configuration = resolve_modes(configuration, modes=modes)
        resolve_none(configuration)
        if build_instances:
            return configuration.build_instances(
                external_configurations=external_configurations, build_key=build_key
            )
        return configuration

    @property
    def name(self):
        return self._name

    def merge(self, config):
        config = ConfigDict(config)
        super().merge(config)

    def build_instances(self, external_configurations=None, build_key=None):
        build = deepcopy(self)

        for mode in self._modes:
            configurations = {self._name: build[mode]}
            if external_configurations is not None:
                for configuration in external_configurations:
                    configurations.update({configuration.name: configuration[mode]})

            build_keys = list(build[mode].keys())
            if build_key is not None:
                index = build_keys.index(build_key) + 1
                build_keys = build_keys[:index]

            for key in build_keys:
                build[mode][key] = build[mode][key].build(configurations)

        build = build.cast()
        if build_key:
            return {mode: build[mode][build_key] for mode in self._modes}
        return {self.name: {mode: build[mode] for mode in self._modes}}


def get_module(module):
    try:
        return importlib.import_module(module)
    except Exception:
        module = Path(module)
        spec = importlib.util.spec_from_file_location(module.stem, str(module))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


def _build_object(builds, module, attribute):
    module = get_module(module.cast())
    attributes = attribute.cast().split(".")
    attribute = module
    for attr in attributes:
        attribute = getattr(attribute, attr)

    if '__return_type' in builds:
        return attribute
    return attribute(**builds.cast())


def _build_registrant_object(
    builds: dict, registrar_module, registrar_name, registrant_module, registrant_name
):
    registrar_module = get_module(registrar_module.cast())
    registrar = getattr(registrar_module, registrar_name.cast())

    # load and register registrant
    if registrant_module is not None:
        _ = get_module(registrant_module.cast())
    builds = builds.cast()
    return registrar.create(registrant_name.cast(), **builds)


def resolve_none(configuration):
    for key, value in configuration.items():
        if issubclass(type(value), UserDict):
            resolve_none(value)
        elif issubclass(type(value), UserString) and value.lower() == "none":
            configuration[key] = ConfigObject(None)


def resolve_modes(config, modes, default_mode=DEFAULT_MODE):
    copied_config = deepcopy(config)
    new_config = Configuration(config.name, dict(), modes=modes)

    if default_mode in copied_config:
        new_config[default_mode] = copied_config[default_mode]
    for mode in modes:
        new_config[mode] = deepcopy(new_config[default_mode])
        if mode in copied_config:
            new_config[mode].merge(copied_config[mode])
    return new_config


def include_configs(config, search_paths=()):
    search_paths = ("",) + search_paths

    for k, v in config.items():
        if isinstance(v, dict):
            include_configs(v, search_paths)

        if isinstance(v, list):
            for v_item in v:
                if isinstance(v_item, dict):
                    include_configs(v_item, search_paths)

        elif isinstance(
            v, str
        ) and ConfigurationFileExtension.is_configuration_extension_path(v):
            config[k] = open_config(v, search_paths)
            include_configs(config, search_paths)
