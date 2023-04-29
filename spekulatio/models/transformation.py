import re

from pydantic import Field
from pydantic import validator

from spekulatio import Model
from spekulatio.registry import obj_registry
from .pattern import Pattern
from .named_pattern import NamedPattern
from .action import Action


class Transformation(Model):
    pattern: Pattern
    action: Action
    output_name_template: str = "{{ input_path.name }}"

    @validator("pattern", pre=True)
    def check_pattern(cls, value):
        if isinstance(value, str):
            try:
                pattern = obj_registry[NamedPattern][value]
            except KeyError:
                raise ValueError(f"Named pattern '{ value }' doesn't exist.")
        else:
            pattern = value
        return pattern

    @validator("output_name_template")
    def check_output_name(cls, value):
        if re.search(r"/|\\", value):
            raise ValueError(
                "'output_name' should only specify a filename template without directories."
            )
        return value
