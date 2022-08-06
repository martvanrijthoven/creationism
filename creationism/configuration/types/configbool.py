
from creationism.configuration.types.configbase import ConfigBase
from creationism.configuration.types.user import UserBool


@ConfigBase.register((bool,))
class ConfigBool(ConfigBase, UserBool):
    ...
