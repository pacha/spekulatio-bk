import pytest

from pydantic import ValidationError

from spekulatio.models import Attribute


def test_attribute_instantiation():
    attribute = Attribute(name="foo", value=3)

    assert attribute.name == "foo"
    assert attribute.value == 3
    assert attribute.scope == "descendants"
    assert attribute.operation == "replace"


def test_attribute_wrong_instantiation():
    with pytest.raises(ValidationError):
        _ = Attribute(name="foo")


def test_attribute_wrong_instantiation_extra_fields():
    with pytest.raises(ValidationError):
        _ = Attribute(name="foo", bar="baz")


def test_attribute_extended_syntax():
    data = {
        "_": "extended-syntax",
        "value": {"number": 3},
        "scope": "children",
        "operation": "merge",
    }
    attribute = Attribute(name="foo", value=data)

    assert attribute.name == "foo"
    assert attribute.value == {"number": 3}
    assert attribute.scope == "children"
    assert attribute.operation == "merge"


def test_attribute_partial_extended_syntax():
    data = {
        "_": "extended-syntax",
        "value": 3,
        "scope": "children",
    }
    attribute = Attribute(name="foo", value=data)

    assert attribute.name == "foo"
    assert attribute.value == 3
    assert attribute.scope == "children"
    assert attribute.operation == "replace"


def test_attribute_wrong_partial_extended_syntax():
    data = {
        "_": "extended-syntax",
        "value": 3,
        "scope": "children",
        "baz": "this",
    }
    with pytest.raises(ValidationError):
        attribute = Attribute(name="foo", value=data)


def test_attribute_wrong_extend_operation():
    data = {
        "_": "extended-syntax",
        "value": 3,
        "operation": "extend",
    }
    with pytest.raises(ValidationError):
        _ = Attribute(name="foo", value=data)


def test_attribute_wrong_merge_operation():
    data = {
        "_": "extended-syntax",
        "value": 3,
        "operation": "merge",
    }
    with pytest.raises(ValidationError):
        _ = Attribute(name="foo", value=data)
