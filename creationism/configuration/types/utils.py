
from creationism.configuration.types.configbase import ConfigBase


def determine_replace(config1: ConfigBase, config2: ConfigBase):
    if config2.replace is not None:
        return config2.replace
    elif config1.replace is not None:
        return config1.replace
    return config2.__class__.REPLACE
