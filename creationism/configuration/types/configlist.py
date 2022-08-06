from collections import UserList
from creationism.configuration.types.configbase import ConfigBase
from creationism.configuration.types.utils import determine_replace



@ConfigBase.register((list, tuple))
class ConfigList(ConfigBase, UserList):

    REPLACE = True

    def __init__(self, config_value, replace=None):
        super().__init__(config_value)
        self._replace = replace
        for idx in range(len(self)):
            self.data[idx] = ConfigBase.create(
                registrant_name=type(self[idx]), config_value=self.data[idx]
            )

    @property
    def replace(self):
        return self._replace

    def merge(self, config_value):
        """merge only possible by replace of extend, due to the ambiguity of list items ids"""

        if not isinstance(config_value, ConfigList):
            raise ValueError("unsupporterd merging of different config types")

        if determine_replace(self, config_value):
            self.data = config_value.data
        else:
            self.data.extend(config_value.data)

    def cast(self):
        return [item.cast() for item in self]

    def build(self, configuration):
        self.data = [item.build(configuration) for item in self.data]
        return self
