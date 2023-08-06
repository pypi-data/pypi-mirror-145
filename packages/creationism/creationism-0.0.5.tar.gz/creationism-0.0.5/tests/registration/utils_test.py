from creationism.registration.utils import Text, chain_functions


class TestTextUtils:
    def test_lower(self):
        assert Text.lower("A") == "a"

    def test_split_capitals_with_underscore(self):
        assert Text.split_capitals_with_underscore("aBCdEf") == "a_B_Cd_Ef"
        assert Text.split_capitals_with_underscore("BCdEF") == "B_Cd_E_F"


def test_chain_functions():
    test_chain_function = lambda x: chain_functions(
        x, Text.split_capitals_with_underscore, Text.lower
    )
    assert test_chain_function("aBCdEf") == "a_b_cd_ef"
