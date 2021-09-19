from pytest import raises
from strar.errors import RegistrantNotRegisteredError
from strar.factory import RegistrantFactory
from strar.utils import Text, chain_functions


class TestErrors:
    def test_empty_register_error(self):
        with raises(RegistrantNotRegisteredError) as errors:

            class A(RegistrantFactory):
                AUTO = True
                CONVERT_NAME = lambda x: chain_functions(
                    x, Text.split_capitals_with_underscore, Text.lower
                )
                REPLACE=True
            A.create("sub_a")


    def test_registrant_not_registered_error(self):
        with raises(RegistrantNotRegisteredError) as errors:

            class A(RegistrantFactory):
                AUTO = True
                CONVERT_NAME = lambda x: chain_functions(
                    x, Text.split_capitals_with_underscore, Text.lower
                )
                REPLACE=True
            class SubA(A):
                pass

            A.create("sub_b")
