from typing import Any
from enum import Enum

from pydantic import root_validator

from spekulatio import Model


class AttributeScope(str, Enum):
    this = "this"
    this_and_children = "this_and_children"
    children = "children"
    this_and_descendants = "this_and_descendants"
    descendants = "descendants"


class AttributeOperation(str, Enum):
    set = "set"  # type: ignore
    set_if_not_exists = "set_if_not_exists"
    merge = "merge"
    prepend = "prepend"
    append = "append"
    delete = "delete"


valid_operations = {
    "set": object,
    "set_if_not_exists": object,
    "merge": dict,
    "prepend": list,
    "append": list,
    "delete": object,
}


class Attribute(Model):
    name: str
    value: Any
    scope: AttributeScope = AttributeScope.this_and_descendants
    operation: AttributeOperation = AttributeOperation.set

    @root_validator(pre=True)
    def check_extended_syntax(cls, items):
        # get name
        try:
            name = items["name"]
        except KeyError:
            raise ValueError(
                "It is necessary to provide a name to define an attribute."
            )

        # get value
        try:
            value = items["value"]
        except KeyError:
            raise ValueError(
                f"It is necessary to provide a value to define attribute '{name}'."
            )

        # check if it is extended syntax
        if isinstance(value, dict) and "_" in value and value["_"] == "extended-syntax":
            # check that there aren't extra keys
            valid_keys = {"_", "name", "value", "scope", "operation"}
            provided_keys = set(value.keys())
            extra_keys = provided_keys - valid_keys
            if extra_keys:
                raise ValueError(
                    f"Found invalid keys '{extra_keys}' in definition of attribute '{name}'"
                )

            # split value into the correct fields
            try:
                extended_items = {
                    "name": name,
                    "value": value["value"],
                }
            except KeyError:
                raise ValueError(
                    f"No value provided in the extended definition of '{name}'"
                )
            else:
                if "scope" in value:
                    extended_items["scope"] = value["scope"]
                if "operation" in value:
                    extended_items["operation"] = value["operation"]
            return extended_items
        return items

    @root_validator
    def check_operation_types(cls, items):
        name = items["name"]
        value = items["value"]
        operation = items["operation"]
        valid_type = valid_operations[operation]
        if not isinstance(value, valid_type):
            raise ValueError(
                f"Wrong type '{type(value).__name__}' for attribute '{name}'."
                f" The only accepted type for operation '{operation}' is '{valid_type.__name__}'"
            )
        return items
