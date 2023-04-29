from typing import Any
from typing import Callable
from importlib import import_module

from pydantic import root_validator
from pydantic import ValidationError

from spekulatio import Model


class Action(Model):
    module: str = "spekulatio"
    name: str
    params: dict[str, Any] = {}
    _function: Callable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # retrieve action function
        module = import_module(self.module)
        self._function = module.actions[self.name].function

    @root_validator()
    def check_name(cls, values):
        module = values["module"]
        name = values["name"]
        params = values["params"]

        # check module
        try:
            module = import_module(module)
        except ModuleNotFoundError:
            raise ValueError(f"Action module '{ module }' not found.")

        # check 'actions' dictionary
        try:
            actions = module.actions
            if not isinstance(actions, dict):
                raise ValueError(
                    f"Wrong action module '{ module }': 'actions' must be a dictionary."
                )
        except AttributeError:
            raise ValueError(
                f"Action module '{ module }' doesn't define a dictionary of actions."
            )

        # check action name
        try:
            action = actions[name]
        except KeyError:
            raise ValueError(f"Action '{ name }' not found.")

        # check params
        try:
            _ = action.params_spec(**params)
        except ValidationError:
            raise

        return values
