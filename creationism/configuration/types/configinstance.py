from creationism.configuration.types.configbase import ConfigBase
from creationism.configuration.types.user import UserInstance


@ConfigBase.register((UserInstance,))
class ConfigInstance(ConfigBase, UserInstance):
    ...
