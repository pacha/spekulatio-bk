from typing import Any
from typing import Callable

from .model import Model
from .models.actions import debug


class ActionSpec(Model):
    function: Callable
    params_spec: Any


actions = {
    "debug": ActionSpec(function=debug.action, params_spec=debug.ActionParamsSpec),
}
