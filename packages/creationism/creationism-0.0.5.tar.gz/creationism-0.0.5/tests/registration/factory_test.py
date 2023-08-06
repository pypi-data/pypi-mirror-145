from creationism.registration.factory import RegistrantFactory
from creationism.registration.utils import Text, chain_functions

class TestRegistrantFactory:

    def test_create_instance(self):
        class A(RegistrantFactory):
            AUTO = True
            CONVERT_NAME = lambda x: chain_functions(
                x, Text.split_capitals_with_underscore, Text.lower
            )
            REPLACE = True

        class SubA(A):
            pass

        suba = A.create('sub_a')
        assert isinstance(suba, SubA)

        
    def test_create_type(self):
        class A(RegistrantFactory):
            AUTO = True
            CONVERT_NAME = lambda x: chain_functions(
                x, Text.split_capitals_with_underscore, Text.lower
            )
            REPLACE = True

        class SubA(A):
            pass

        suba = A.create('sub_a',return_type=True)
        assert SubA is suba

        
    def test_create_static_instance(self):
        class A(RegistrantFactory):
            AUTO = True
            CONVERT_NAME = lambda x: chain_functions(
                x, Text.split_capitals_with_underscore, Text.lower
            )
            REPLACE = True
            STATIC=True
            

        class SubA(A):
            pass

        suba = A.create('sub_a')
        suba2 = A.create('sub_a')
        assert suba is suba2
    
    def test_create_non_static_instance(self):
        class A(RegistrantFactory):
            AUTO = True
            CONVERT_NAME = lambda x: chain_functions(
                x, Text.split_capitals_with_underscore, Text.lower
            )
            REPLACE = True
            STATIC=False

        class SubA(A):
            pass

        suba = A.create('sub_a')
        suba2 = A.create('sub_a')
        assert suba is not suba2
