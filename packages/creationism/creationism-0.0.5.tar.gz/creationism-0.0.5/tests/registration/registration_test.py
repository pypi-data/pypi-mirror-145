from creationism.configuration.extensions import ConfigurationFileExtension, JsonConfigurationFileExtension
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



    def test_decorator_register_recursive(self):
        class A(RegistrantFactory):
            AUTO = False

        @A.register(("suba",), recursive=True)
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


    def test_create_from_subclass(self):
        assert JsonConfigurationFileExtension is ConfigurationFileExtension.create(JsonConfigurationFileExtension, return_type=True)

    def test_create_from_subclass2(self):
        json_config_extension = JsonConfigurationFileExtension()
        assert json_config_extension is ConfigurationFileExtension.create(json_config_extension)

    def test_get_registrant(self):
        assert JsonConfigurationFileExtension is ConfigurationFileExtension.get_registrant(JsonConfigurationFileExtension)

    def test_register_func(self):

        class A(RegistrantFactory):
            @classmethod
            def create(cls, a):
                return super().create(registrant_name=type(a), a=a)

            def __init__(self, a):
                self.a = a

        @A.register_func((dict,))
        def create_a_from_type(a):
            return A(a)

        assert {} == A.create({}).a