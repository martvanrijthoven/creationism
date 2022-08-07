import os
import pathlib
from collections import UserList
from copy import deepcopy
from pathlib import Path

from creationism.configuration.extensions import ConfigurationFileExtension, open_config
from creationism.configuration.types import ConfigDict, ConfigNone, ConfigString
from creationism.mode import DEFAULT_MODE


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
        super().__init__(data=config_value)

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


def resolve_none(configuration):
    if type(configuration) == ConfigDict:
        for key, value in configuration.items():
            if type(value) == ConfigString and value.lower() == "none":
                configuration[key] = ConfigNone(None)
            else:
                resolve_none(value)
    elif type(configuration) == UserList:
        for value in configuration:
            resolve_none(value)


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
