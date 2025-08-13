import configparser
from pathlib import Path

_test_config = configparser.ConfigParser()

config_path = Path(__file__).parent / "test_config.ini"
_test_config.read(config_path)

def get_value(section, key):
    return _test_config.get['pages'],['loginpage_heading']