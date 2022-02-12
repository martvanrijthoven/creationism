from creationism.registration.factory import RegistrantFactory
from creationism.registration.utils import Text, chain_functions


class TestRegistrar:
    def test_not_auto_register(self):
        class A(RegistrantFactory):
            AUTO = False

        class SubA(A):
            pass

        assert A._REGISTER is None

    def test_auto_register(self):
        class A(RegistrantFactory):
            AUTO = True
            CONVERT_NAME = lambda x: chain_functions(
                x, Text.split_capitals_with_underscore, Text.lower
            )

        class SubA(A):
            pass

        assert A._REGISTER is not None
        assert "sub_a" in A._REGISTER
        assert SubA in A._REGISTER.values()

    def test_decorator_register(self):
        class A(RegistrantFactory):
            AUTO = False

        @A.register(("suba",))
        class SubA(A):
            pass

        assert A._REGISTER is not None
        assert "suba" in A._REGISTER
        assert SubA in A._REGISTER.values()



    def test_name(self):
        class A(RegistrantFactory):
            AUTO = True

        class SubA(A):
            pass

        sub_a = SubA()
        assert sub_a.name == 'SubA'



    def test_convert_name_name(self):
        class A(RegistrantFactory):
            AUTO = True
            CONVERT_NAME = lambda x: chain_functions(
                x, Text.split_capitals_with_underscore, Text.lower
            )

        class SubA(A):
            pass

        sub_a = SubA()
        assert sub_a.name == "sub_a"


