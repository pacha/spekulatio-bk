from pathlib import Path

import pytest
from pydantic import ValidationError

from spekulatio.models import PatternRegistry
from spekulatio.models import Transformation


def test_named_pattern_registration():
    pattern_registry = PatternRegistry(patterns=[
        {
            "name": "jpeg",
            "type": "regex",
            "value": r"^.*\.(jpeg|jpg)",
        }
    ])

    # create a transformation
    transformation = Transformation(
        pattern_registry=pattern_registry,
        **{
            "pattern": "jpeg",
            "action": {
                "name": "debug",
            },
        }
    )
    assert transformation.pattern.match(Path("/foo/bar.jpeg"))


def test_missing_named_pattern():
    pattern_registry = PatternRegistry(patterns=[
        {
            "name": "jpeg",
            "type": "regex",
            "value": r"^.*\.(jpeg|jpg)",
        }
    ])

    # create a transformation
    with pytest.raises(ValidationError):
        _ = Transformation(
            pattern_registry=pattern_registry,
            **{
                "pattern": "md",
                "action": {
                    "name": "debug",
                },
            }
        )
