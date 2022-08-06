from creationism.configuration.types.configbase import ConfigBase
from creationism.configuration.types.user import UserFloat

@ConfigBase.register((float,))
class ConfigFloat(ConfigBase, UserFloat):
    ...
