from creationism.registration.factory import RegistrantFactory
from creationism.registration.utils import Text, chain_functions
from functools import partial

class ConfigBase(RegistrantFactory):
    CONVERT_NAME = lambda x: chain_functions(
        x, Text.split_capitals, Text.lower, Text.split, partial(Text.get, index=-1)
    )

    def merge(self, config_value):
        self.data = config_value.data

    def cast(self):
        return self.data

    def build(self, configuration):
        return self