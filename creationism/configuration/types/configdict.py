import re
from collections import UserDict

from creationism.configuration.build import build_object, build_registrant_object
from creationism.configuration.constants import REPLACE_IDENTIFIER
from creationism.configuration.types.configbase import ConfigBase, ConfigObject



@ConfigBase.register((dict,))
class ConfigDict(ConfigBase, UserDict):
    REPLACE = False

    def __init__(self, data, replace=None):
        super().__init__(dict(), replace=replace)
        self._iterative_init(data=data)

    def _iterative_init(self, data):
        for key in list(data):
            class_type = type(data[key])
            replace = re.search(REPLACE_IDENTIFIER, key)
            if replace:
                key_stripped = key.replace(replace.group(0), "")
                replace = replace.group(1).lower() == "true"
                self.data[key_stripped] = ConfigBase.create(
                    registrant_name=class_type,
                    data=data[key],
                    replace=replace,
                )
            else:
                self.data[key] = ConfigBase.create( 
                    registrant_name=class_type, data=data[key]
                )

    def merge(self, config_value):
        if not isinstance(config_value, ConfigDict):
            raise ValueError("unsupporterd merging of different config types")
        else:
            self._iterative_merge(config_value)

    def _iterative_merge(self, config_value):

        if self.determine_replace(config_value):
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
                build_registrant_object(
                    self,
                    registrar_module,
                    registrar_name,
                    registrant_module,
                    registrant_name,
                )
            )

        if module is not None and attribute is not None:
            return ConfigObject(build_object(self, module, attribute))

        return self
