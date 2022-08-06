
from creationism.configuration.types.configbase import ConfigBase
from creationism.configuration.types.user import UserInt


@ConfigBase.register((int,))
class ConfigInt(ConfigBase, UserInt):
    ...
