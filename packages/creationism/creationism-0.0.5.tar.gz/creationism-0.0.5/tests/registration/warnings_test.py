from pytest import warns
from creationism.registration.factory import RegistrantFactory
from creationism.registration.utils import Text, chain_functions
from creationism.registration.warnings import DuplicateRegistrantNameWarning


class TestWarnings:
    def test_no_replace(self):
        with warns(DuplicateRegistrantNameWarning):

            class A(RegistrantFactory):
                AUTO = False
                CONVERT_NAME = lambda x: x
                REPLACE = False

            @A.register(("suba", "suba"))
            class SubA(A):
                pass

        with warns(DuplicateRegistrantNameWarning):

            class A(RegistrantFactory):
                AUTO = True
                CONVERT_NAME = lambda x: chain_functions(
                    x, Text.split_capitals_with_underscore, Text.lower
                )
                REPLACE = False

            @A.register(("sub_a",))
            class SubA(A):
                pass

    def test_replace(self):

        with warns(None) as record:

            class A(RegistrantFactory):
                AUTO = False
                CONVERT_NAME = lambda x: chain_functions(
                    x, Text.split_capitals_with_underscore, Text.lower
                )
                REPLACE = True

            @A.register(("sub_a",))
            class SubA(A):
                pass

            assert len(record) == 0

        with warns(None) as record:

            class A(RegistrantFactory):
                AUTO = False
                CONVERT_NAME = lambda x: x
                REPLACE = True

            @A.register(("suba", "suba"), replace=True)
            class SubA(A):
                pass

        assert len(record) == 0
