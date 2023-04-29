import pytest
from pydantic import ValidationError

from spekulatio.models import Preset
from spekulatio.models import InputDir
from spekulatio.models import Transformation


def test_preset_registration(fixtures_path):
    # patterns are globally registered by default if they have a name
    preset = Preset(
        **{
            "name": "site-content",
            "transformations": [
                {
                    "pattern": {
                        "type": "glob",
                        "value": "*.md",
                    },
                    "action": {
                        "name": "debug",
                        "params": {},
                    },
                    "output_name_template": "{{ input_path.stem }}.html",
                }
            ],
        }
    )

    # create an input dir
    input_dir = InputDir(
        root_path=fixtures_path,
        **{
            "path": "empty-input-dir",
            "preset": "site-content",
            "transformations": [
                {
                    "pattern": {
                        "type": "glob",
                        "scope": "filename",
                        "value": "*.md",
                    },
                    "action": {
                        "name": "debug",
                    },
                    "output_name_template": "{{ input_path.stem }}.html",
                }
            ],
        }
    )
    assert input_dir.preset == preset


def test_missing_preset(fixtures_path):
    # try to create an input dir based on a non-existent preset
    with pytest.raises(ValidationError):
        _ = InputDir(
            root_path=fixtures_path,
            **{
                "path": "empty-input-dir",
                "preset": "non-existing-preset",
                "transformations": [
                    {
                        "pattern": {
                            "type": "glob",
                            "scope": "filename",
                            "value": "*.md",
                        },
                        "action": {
                            "name": "debug",
                        },
                        "output_name": "{{ input_path.stem }}.html",
                    }
                ],
            }
        )
