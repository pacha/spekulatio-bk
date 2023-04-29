import pytest
from pydantic import ValidationError

from spekulatio.models import Action
from spekulatio.models.actions.debug import action as debug_action_function


def test_action_name():
    action = Action(
        **{
            "name": "debug",
            "params": {"foo": "bar"},
        }
    )
    assert action._function == debug_action_function
    assert action.params["foo"] == "bar"


def test_wrong_action_name():
    with pytest.raises(ValidationError) as err:
        _ = Action(
            **{
                "name": "foobar",
            }
        )
    assert "Action 'foobar' not found." in err.value.errors()[0]["msg"]


def test_wrong_action_module():
    with pytest.raises(ValidationError) as err:
        _ = Action(
            **{
                "module": "foobar",
                "name": "debug",
                "params": {},
            }
        )
    assert "Action module 'foobar' not found." in err.value.errors()[0]["msg"]
