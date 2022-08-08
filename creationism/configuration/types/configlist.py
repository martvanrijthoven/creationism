from collections import UserList
from creationism.configuration.types.configbase import ConfigBase


@ConfigBase.register((list, tuple))
class ConfigList(ConfigBase, UserList):

    REPLACE = True

    def __init__(self, name, data, replace=None):
        super().__init__(name, data, replace=replace)
        for idx in range(len(self)):
            self.data[idx] = ConfigBase.create(
                name=name+'_'+str(idx), registrant_name=type(self[idx]), data=self.data[idx]
            )

    def merge(self, config_value):
        """merge only possible by replace of extend, due to the ambiguity of list items ids"""

        if not isinstance(config_value, ConfigList):
            raise ValueError("unsupporterd merging of different config types")

        if self.determine_replace(config_value):
            self.data = config_value.data
        else:
            self.data.extend(config_value.data)

    def cast(self):
        return [item.cast() for item in self]

    def build(self, configuration):
        self.data = [item.build(configuration) for item in self.data]
        return self
