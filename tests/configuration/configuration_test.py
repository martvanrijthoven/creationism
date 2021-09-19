from creationism.configuration.config import ConfigDict
from pathlib import Path


class TestConfig:
    def test_create_config_dict(self):
        config = {"a": 1, "b": "b", "c": [1, 2, 3]}
        config_dict = ConfigDict(config_value=config)
        assert isinstance(config_dict, ConfigDict)

    def test_create_config_dict_with_replace_is_true_list(self):
        config = {"a": 1, "b": "b", "c[replace=true]": [1, 2, 3]}
        config_dict = ConfigDict(config_value=config)
        assert config_dict["c"].replace is True

    def test_create_config_dict_with_replace_is_false_list(self):
        config = {"a": 1, "b": "b", "c[replace=false]": [1, 2, 3]}
        config_dict = ConfigDict(config_value=config)
        assert config_dict["c"].replace is False

    def test_create_config_dict_with_replace_is_true_dict(self):
        config = {"a": 1, "b": "b", "c[replace=true]": {"c2": "hello"}}
        config_dict = ConfigDict(config_value=config)
        assert config_dict["c"].replace is True

    def test_create_config_dict_with_replace_is_true_dict(self):
        config = {"a": 1, "b": "b", "c[replace=false]": {"c2": "hello"}}
        config_dict = ConfigDict(config_value=config)
        assert config_dict["c"].replace is False

    def test_create_config_dict_with_yaml_reference(self):
        config = {"a": 1, "b": "b", "c": str(Path(__file__).parent / "test.yml")}
        config_dict = ConfigDict(config_value=config).cast()
        assert config_dict["c"]["name"] == [1,2,3]

    def test_create_config_dict_with_yaml_reference_replace(self):
        config = {"a": 1, "b": "b", "c": str(Path(__file__).parent / "test.yml")}
        config_dict = ConfigDict(config_value=config)
        assert config_dict["c"]["name"].replace is False


    def test_merge_replace_dict_true(self):
        config = {"a": 1, "b": "b", "c": {'k': {'n': 4}}}
        config2 = {"a": 1, "b": "b", "c[replace=true]": {'k': {'l': 5}}}
        config_dict = ConfigDict(config_value=config)
        config_dict2 = ConfigDict(config_value=config2)
        config_dict.merge(config_dict2)
        assert config_dict["c"]["k"]['l'].cast() == 5
        assert 'n' not in config_dict["c"]["k"]

    # def test_merge_replace_dict_false(self):
    #     config = {"a": 1, "b": "b", "c": str(Path(__file__).parent / "test.yml")}
    #     config_dict = ConfigDict(config_value=config)
    #     assert config_dict["c"]["name"].replace is False


    # def test_merge_replace_list_true(self):
    #     config = {"a": 1, "b": "b", "c": str(Path(__file__).parent / "test.yml")}
    #     config_dict = ConfigDict(config_value=config)
    #     assert config_dict["c"]["name"].replace is False

    # def test_merge_replace_list_false(self):
    #     config = {"a": 1, "b": "b", "c": str(Path(__file__).parent / "test.yml")}
    #     config_dict = ConfigDict(config_value=config)
    #     assert config_dict["c"]["name"].replace is False



    # def test_cast_config_dict(self):
