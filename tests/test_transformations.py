from pathlib import Path

import pytest
from pydantic import ValidationError

from spekulatio.models import Transformation


def test_instantiation():
    transformation = Transformation(
        **{
            "pattern": {
                "type": "glob",
                "scope": "filename",
                "value": "*.md",
            },
            "action": {
                "name": "debug",
                "params": {},
            },
            "output_name_template": "{{ input_path.stem }}.html",
        }
    )
    assert transformation.output_name_template == "{{ input_path.stem }}.html"


def test_minimal_instantiation():
    transformation = Transformation(
        **{
            "pattern": {
                "value": "*.md",
            },
            "action": {
                "name": "debug",
            },
        }
    )
    assert transformation.output_name_template == "{{ input_path.name }}"


def test_wrong_pattern():
    with pytest.raises(ValidationError):
        _ = Transformation(
            **{
                "pattern": {
                    "scope": "filename",
                },
                "action": {
                    "name": "debug",
                },
            }
        )


def test_wrong_action():
    with pytest.raises(ValidationError):
        _ = Transformation(
            **{
                "pattern": {
                    "value": "*.md",
                },
                "action": {
                    "name": "debug",
                    "foo": "bar",
                },
            }
        )


def test_wrong_output_name():
    with pytest.raises(ValidationError):
        transformation = Transformation(
            **{
                "pattern": {
                    "value": "*.md",
                },
                "action": {
                    "name": "debug",
                },
                "output_name_template": "some/folder/{{ input_path.stem }}.html",
            }
        )


def test_wrong_output_name_win_anchor():
    with pytest.raises(ValidationError):
        transformation = Transformation(
            **{
                "pattern": {
                    "value": "*.md",
                },
                "action": {
                    "name": "debug",
                },
                "output_name_template": "some\\folder\\{{ input_path.stem }}.html",
            }
        )
