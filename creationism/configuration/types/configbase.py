from creationism.registration.factory import RegistrantFactory
from creationism.registration.utils import Text, chain_functions
from functools import partial


class ConfigBase(RegistrantFactory):
    CONVERT_NAME = lambda x: chain_functions(
        x, Text.split_capitals, Text.lower, Text.split, partial(Text.get, index=-1)
    )

    def __init__(self, name, data, replace=None):
        self.data = data
        self._replace = replace
        self._name= name

    @property
    def name(self):
        return self._name

    @property
    def replace(self):
        return self._replace

    def merge(self, config_value):
        self.data = config_value.data

    def cast(self):
        return self.data

    def build(self, configuration):
        return self

    def determine_replace(self, config2: "ConfigBase"):
        if config2.replace is not None:
            return config2.replace
        elif self.replace is not None:
            return self.replace
        return config2.__class__.REPLACE



class ConfigObject(ConfigBase):
    ...


@ConfigBase.register((int,))
class ConfigInt(ConfigBase):
    ...


@ConfigBase.register((float,))
class ConfigFloat(ConfigBase):
    ...


@ConfigBase.register((bool,))
class ConfigBool(ConfigBase):
    ...


@ConfigBase.register((type(None),))
class ConfigNone(ConfigBase):
    ...
