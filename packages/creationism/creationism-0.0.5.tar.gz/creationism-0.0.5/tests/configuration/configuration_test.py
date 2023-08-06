import os
from creationism.configuration.config import Configuration
from creationism.configuration.config import open_config
from creationism.configuration.extensions import ConfigurationFileExtension, JsonConfigurationFileExtension
from creationism.mode import Mode, DefaultMode
from pathlib import Path

from creationism.utils import create_name_from_class_name


class TestConfig:
    def test_create_config_dict(self):
        config = {"a": 1, "b": "b", "c": [1, 2, 3]}
        config_dict = Configuration(name='', config_value=config, modes=('default',))
        assert isinstance(config_dict, Configuration)

    def test_create_config_dict_with_replace_is_true_list(self):
        config = {"a": 1, "b": "b", "c@replace=true": [1, 2, 3]}
        config_dict = Configuration(name='', config_value=config, modes=('default',))
        assert config_dict["c"].replace is True

    def test_create_config_dict_with_replace_is_false_list(self):
        config = {"a": 1, "b": "b", "c@replace=false": [1, 2, 3]}
        config_dict = Configuration(name='', config_value=config, modes=('default',))
        assert config_dict["c"].replace is False

    def test_create_config_dict_with_replace_is_true_dict(self):
        config = {"a": 1, "b": "b", "c@replace=true": {"c2": "hello"}}
        config_dict = Configuration(name='', config_value=config, modes=('default',))
        assert config_dict["c"].replace is True

    def test_create_config_dict_with_replace_is_true_dict(self):
        config = {"a": 1, "b": "b", "c@replace=false": {"c2": "hello"}}
        config_dict = Configuration(name='', config_value=config, modes=('default',))
        assert config_dict["c"].replace is False

    def test_create_config_dict_with_yaml_reference(self):
        config = {"a": 1, "b": "b", "c": str(Path(__file__).parent / "test.yml")}
        config_dict = Configuration(name='', config_value=config, modes=('default',)).cast()
        assert config_dict["c"]["name"] == [1, 2, 3]

    def test_create_config_dict_with_yaml_reference_replace(self):
        config = {"a": 1, "b": "b", "c": str(Path(__file__).parent / "test.yml")}
        config_dict = Configuration(name='', config_value=config, modes=('default',))
        assert config_dict["c"]["name"].replace is False

    def test_merge_replace_dict_true(self):
        config = {"a": 1, "b": "b", "c": {"k": {"n": 4}}}
        config_dict = Configuration(name='1', config_value=config, modes=('default',))

        config2 = {"a": 1, "b": "b", "c@replace=true": {"k": {"l": 5}}}
        config_dict.merge(config2)
        assert config_dict["c"]["k"]["l"].cast() == 5
        assert "n" not in config_dict["c"]["k"]

    def test_merge_replace_dict_false(self):
        config = {"a": 1, "b": "b", "c": str(Path(__file__).parent / "test.yml")}
        config_dict = Configuration(name='', config_value=config, modes=('default',))
        assert config_dict["c"]["name"].replace is False

    def test_merge_replace_list_true(self):
        config = {"a": 1, "b": "b", "c": str(Path(__file__).parent / "test.yml")}
        config_dict = Configuration(name='', config_value=config, modes=('default',))
        assert config_dict["c"]["name"].replace is False

    def test_merge_replace_list_false(self):
        config = {"a": 1, "b": "b", "c": str(Path(__file__).parent / "test.yml")}
        config_dict = Configuration(name='', config_value=config, modes=('default',))
        assert config_dict["c"]["name"].replace is False

    def test_has_extension(self):
        user_config = Path(__file__).parent / "testobject.json"
        assert True == ConfigurationFileExtension.has_extension(user_config, JsonConfigurationFileExtension)

    def test_is_extension(self):
        assert True == ConfigurationFileExtension.is_extension('.json', JsonConfigurationFileExtension)

    def test_create_name_from_class(self):
        assert 'Json Configuration File' == create_name_from_class_name('JsonConfigurationFileExtension')

    def test_build_config(self):
        user_config = str(Path(__file__).parent / "testobject.json")
        config_value = open_config(user_config, search_paths=('./', ))
        configuration = Configuration(name='configuration', config_value=config_value, modes=('default',))
        builds = configuration.build_instances()
        assert builds['configuration']['default']['mode'] is Mode.create('default')

    def test_build_config_class(self):
        _DEFAULT_MODES = ("test",)
        class TestConfiguration(Configuration):
            NAME = "testconfiguration"
            PRESETS_FOLDER = Path(__file__).absolute().parent / "presets"
            CONFIG_PATH = Path(__file__).absolute().parent / os.path.join(
                "config_files", "config.yml"
            )

            SEARCH_PATHS = ("", Path(__file__).absolute().parent / "config_files")

            def __init__(self, modes=_DEFAULT_MODES, search_paths=()):

                search_paths_ = self.__class__.SEARCH_PATHS + search_paths
                config_value = open_config(
                    TestConfiguration.CONFIG_PATH, search_paths=search_paths_
                )

                super().__init__(
                    name=TestConfiguration.NAME,
                    modes=modes,
                    config_value=config_value,
                    search_paths=search_paths,
                )
        


        user_config = str(Path(__file__).parent / "testobject.json")
        config_value = open_config(user_config, search_paths=('./', ))
        user_config_dict = open_config(user_config, search_paths=('./', ))
        configuration = Configuration(name='configuration', config_value=config_value, modes=('default',))
        builds_external = TestConfiguration.build(user_config=user_config_dict, modes=('default',), external_configurations=(configuration, ))

        user_config = str(Path(__file__).parent / "testobject2.yml")
        build_builder = TestConfiguration.build(user_config=user_config_dict, modes=('test',), build_instances=False)
        builds = TestConfiguration.build(user_config=user_config, modes=('test',), presets=('aisb', ))
        builds = TestConfiguration.build(user_config=user_config_dict, modes=('test',), search_paths=('./', ))


        ref = TestConfiguration.build(user_config=user_config, modes=('test',), build_key='ref')

        assert isinstance(ref['test'], DefaultMode)
