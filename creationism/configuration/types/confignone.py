
from creationism.configuration.types.configbase import ConfigBase
from creationism.configuration.types.user import UserNone


@ConfigBase.register((type(None),))
class ConfigNone(ConfigBase, UserNone):
    ...
