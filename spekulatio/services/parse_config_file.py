
from pathlib import Path

import yaml
from pydantic import validator
from pydantic import ValidationError

from spekulatio import Model
from spekulatio.models import NamedPattern
from spekulatio.models import PatternRegistry
from spekulatio.models import InputDir
from spekulatio.models import OutputDir
from spekulatio.errors import SpekulatioConfigError


class Config(Model):
    root_path: Path
    patterns: list[NamedPattern] = []
    output_dir: OutputDir
    input_dirs: list[InputDir] = []

    @validator("output_dir", pre=True)
    def check_output_dir(cls, value, values):
        try:
            value['root_path'] = values['root_path']
        except Exception as err:
            raise ValueError(f"'output_dir' must be a dictionary of values ({err}).")
        return value

    @validator("input_dirs", pre=True)
    def check_input_dirs(cls, value, values):
        root_path = values['root_path']
        patterns = values['patterns']
        try:
            for input_dir_dict in value:
                input_dir_dict['root_path'] = root_path
                input_dir_dict['pattern_registry'] = PatternRegistry(patterns=patterns)
        except Exception as err:
            raise ValueError(f"'input_dirs' must be a list of dictionaries ({err})")
        return value

def parse_config_file(path: Path, config_overrides: dict = {}) -> Config:
    # read content
    try:
        config_yaml = path.read_text()
    except Exception as err:
        raise SpekulatioConfigError(f"Can't read configuration file '{path}' ({err})")

    # parse yaml
    try:
        config_dict = yaml.safe_load(config_yaml) or {}
    except Exception as err:
        raise SpekulatioConfigError(f"Can't parse configuration file '{path}' ({err})")

    # merge overrides
    try:
        config_dict.update(config_overrides)
    except Exception as err:
        raise SpekulatioConfigError(f"Configuration file is not a dictionary of values ({err})")

    # get configuration object
    root_path = path.parent
    try:
        config = Config(root_path=root_path, **config_dict)
    except ValidationError as err:
        raise SpekulatioConfigError(f"Configuration error:\n{err}")

    return config
