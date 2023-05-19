
import pytest

from spekulatio.services import parse_config_file
from spekulatio.errors import SpekulatioConfigError


def test_empty_config(fixtures_path):
    spekulatio_file = fixtures_path / "config" / "empty-config.yaml"
    # an entry for input_dirs is mandatory (even if it is an empty list)
    with pytest.raises(SpekulatioConfigError):
        _ = parse_config_file(spekulatio_file)

def test_only_input_dirs_config(fixtures_path):
    spekulatio_file = fixtures_path / "config" / "only-input-dirs.yaml"
    # output_dir is mandatory if not provided through command line
    with pytest.raises(SpekulatioConfigError):
        _ = parse_config_file(spekulatio_file)

def test_overriden_output_dir_config(fixtures_path):
    spekulatio_file = fixtures_path / "config" / "overriden-output-dir" / "spekulatio.yaml"
    # config overrides are used to pass config values passed through command line
    config_overrides = {
        "output_dir": {
            "path": str(fixtures_path / "config" / "overriden-output-dir" / "output-dir")
        }
    }
    config = parse_config_file(spekulatio_file, config_overrides)
    assert config.output_dir.path.is_dir()

def test_minimal_config(fixtures_path):
    spekulatio_file = fixtures_path / "config" / "minimal-config" / "spekulatio.yaml"
    config = parse_config_file(spekulatio_file)
    assert config.output_dir.path.is_dir()

def test_full_config(fixtures_path):
    spekulatio_file = fixtures_path / "config" / "full-config" / "spekulatio.yaml"
    config = parse_config_file(spekulatio_file)
    assert config.output_dir.path.is_dir()

