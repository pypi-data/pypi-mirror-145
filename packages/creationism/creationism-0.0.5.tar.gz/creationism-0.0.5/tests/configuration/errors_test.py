from creationism.configuration.config import Configuration
from creationism.configuration.extensions import open_config
from pathlib import Path
from pytest import raises


class TestConfigError:
    def test_build_config_class(self):

        with raises(ValueError) as errors:
            config = {"a": [1, 2, 3]}
            config_dict = Configuration(
                name="1", config_value=config, modes=("default",)
            )

            config2 = {"a": {1, 2, 3}}
            config_dict.merge(config2)

    def test_build_config_class2(self):
        with raises(ValueError) as errors:
            config = {"a": "hello", "b": {"c": {1, 2, 3}}}
            config_dict = Configuration(
                name="1", config_value=config, modes=("default",)
            )

            config2 = {"b": [1, 2, 3]}
            config_dict.merge(config2)

    def test_build_config_not_found(self):
        with raises(FileNotFoundError) as errors:
            user_config = str(Path(__file__).parent / "testobject2.json")
            config_value = open_config(user_config, search_paths=("./",))
            configuration = Configuration(
                name="configuration", config_value=config_value, modes=("default",)
            )
            builds = configuration.build_instances()
