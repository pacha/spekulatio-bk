from pathlib import Path

import pytest
from pydantic import ValidationError

from spekulatio.models import NamedPattern
from spekulatio.models import Transformation


def test_named_pattern_registration():
    # patterns are globally registered by default if they have a name
    _ = NamedPattern(
        **{
            "name": "jpeg",
            "type": "regex",
            "value": r"^.*\.(jpeg|jpg)",
        }
    )

    # create a transformation
    transformation = Transformation(
        **{
            "pattern": "jpeg",
            "action": {
                "name": "debug",
            },
        }
    )
    assert transformation.pattern.match(Path("/foo/bar.jpeg"))


def test_missing_named_pattern():
    # patterns are globally registered by default if they have a name
    _ = NamedPattern(
        **{
            "name": "jpeg",
            "type": "regex",
            "value": r"^.*\.(jpeg|jpg)",
        }
    )

    # create a transformation
    with pytest.raises(ValidationError):
        _ = Transformation(
            **{
                "pattern": "md",
                "action": {
                    "name": "debug",
                },
            }
        )
