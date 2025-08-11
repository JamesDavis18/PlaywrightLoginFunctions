import configparser
from pathlib import Path

_test_config = configparser.ConfigParser()
_test_config.read(Path.parent / "tests" / "test_config.ini")

def get_value(section, key):
    return _test_config.get[section],[key]