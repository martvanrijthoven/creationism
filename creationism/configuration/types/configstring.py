import operator
from collections import UserString
from functools import reduce

from creationism.configuration.constants import (
    REFERENCE_ATTRIBUTE_SYMBOL,
    REFERENCE_MAP_SYMBOL,
    REFERENCE_START_SYMBOL,
)
from creationism.configuration.types.configbase import ConfigBase, ConfigObject


@ConfigBase.register((str,))
class ConfigString(ConfigBase, UserString):
    def merge(self, config_value):
        self.data = config_value.data

    def cast(self):
        return self.data

    def build(self, configuration):
        if REFERENCE_START_SYMBOL == self.data[0]:
            return self._get_reference(configuration)
        return self

    def _get_reference(self, configuration):
        self.data = self.data.replace("{", "").replace("}", "")
        references = self.data[1:].split(REFERENCE_MAP_SYMBOL)
        reference = reduce(operator.getitem, references[:-1], configuration)
        attributes = references[-1].split(REFERENCE_ATTRIBUTE_SYMBOL)
        reference = reference[attributes[0]].cast()
        for attr in attributes[1:]:
            reference = getattr(reference, attr)
        return ConfigObject(name=self.name, data=reference)
