from pathlib import Path

import pytest

from spekulatio.models import Pattern


def test_pattern_value_as_str():
    pattern_data = {
        "type": "regex",
        "value": r"^.*\.(jpeg|jpg)",
    }
    pattern = Pattern(**pattern_data)
    assert pattern.match(Path("file.jpeg"))
    assert pattern.match(Path("file.jpg"))


def test_pattern_value_as_list():
    pattern_data = {
        "type": "regex",
        "value": [
            r"^.*\.jpeg",
            r"^.*\.jpg",
        ],
    }
    pattern = Pattern(**pattern_data)
    assert pattern.match(Path("file.jpeg"))
    assert pattern.match(Path("file.jpg"))


def test_regex_match():
    pattern_data = {
        "type": "regex",
        "value": r"^.*\.(jpeg|jpg)",
    }
    pattern = Pattern(**pattern_data)

    assert pattern.match(Path("file.jpeg"))
    assert pattern.match(Path("file.jpg"))
    assert not pattern.match(Path("file.png"))


def test_glob_match():
    pattern_data = {
        "type": "glob",
        "value": [
            "*.jpeg",
            "*.jpg",
        ],
    }
    pattern = Pattern(**pattern_data)

    assert pattern.match(Path("file.jpeg"))
    assert pattern.match(Path("file.jpg"))
    assert not pattern.match(Path("file.png"))


def test_literal_match():
    pattern_data = {
        "type": "literal",
        "value": [
            "file.jpeg",
            "file.jpg",
        ],
    }
    pattern = Pattern(**pattern_data)

    assert pattern.match(Path("file.jpeg"))
    assert pattern.match(Path("file.jpg"))
    assert not pattern.match(Path("file.png"))


def test_pattern_path_scope():
    pattern_data = {
        "type": "regex",
        "scope": "path",
        "value": r"foo/.*/baz.txt",
    }
    pattern = Pattern(**pattern_data)

    assert pattern.match(Path("foo/spam/baz.txt"))
    assert not pattern.match(Path("bar/spam/baz.txt.jpg"))
    assert not pattern.match(Path("foo/baz.txt"))
    assert not pattern.match(Path("bar/baz.txt.jpg"))
    assert not pattern.match(Path("baz.txt"))


def test_pattern_filename_scope():
    pattern_data = {
        "type": "regex",
        "scope": "filename",
        "value": r"a..b\.txt",
    }
    pattern = Pattern(**pattern_data)

    assert pattern.match(Path("aabb.txt"))
    assert pattern.match(Path("foo/bar/aabb.txt"))
    assert not pattern.match(Path("babb.txt"))
    assert not pattern.match(Path("a/bb.txt"))


def test_pattern_extension_scope():
    pattern_data = {
        "type": "regex",
        "scope": "extension",
        "value": [
            r"\.j.eg",
            r"\.j.g",
        ],
    }
    pattern = Pattern(**pattern_data)

    assert pattern.match(Path("foobar.jpeg"))
    assert pattern.match(Path("foobar.jpg"))
    assert pattern.match(Path("spam/foobar.jpeg"))
    assert not pattern.match(Path("jpeg"))
    assert not pattern.match(Path("spam/foobar.txt"))
