import re
from enum import Enum
from pathlib import Path

from pydantic import validator

from spekulatio import Model
from spekulatio.lib.get_regex import get_regex_from_glob_list
from spekulatio.lib.get_regex import get_regex_from_regex_list
from spekulatio.lib.get_regex import get_regex_from_literal_list


class PatternType(str, Enum):
    glob = "glob"
    regex = "regex"
    literal = "literal"


class PatternScope(str, Enum):
    path = "path"
    filename = "filename"
    extension = "extension"


class Pattern(Model):
    type: PatternType = PatternType.glob
    scope: PatternScope = PatternScope.filename
    value: list[str]
    _regex: re.Pattern

    @validator("value", pre=True)
    def check_value(cls, value):
        # internally, value is always a list, independently
        # of what has been provided
        values = [value] if isinstance(value, str) else value

        # double slashes so that proper literal regex strings
        # can be written by users (eg. "file\.txt" instead of "file\\.txt")
        # values = [value.replace('\\', '\\\\') for value in values]
        return values

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # compile regex
        translators = {
            "glob": get_regex_from_glob_list,
            "regex": get_regex_from_regex_list,
            "literal": get_regex_from_literal_list,
        }
        try:
            translator = translators[self.type]
        except IndexError:
            raise NotImplementedError(self.value)
        self._regex = translator(self.value)

    def match(self, path: Path) -> bool:
        extractors = {
            PatternScope.path: lambda path: str(path),
            PatternScope.filename: lambda path: str(path.name),
            PatternScope.extension: lambda path: str(path.suffix),
        }
        part = extractors[self.scope](path)
        return bool(self._regex.match(part))
