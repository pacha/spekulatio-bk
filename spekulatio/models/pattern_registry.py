
from spekulatio import Model

from . import NamedPattern


class PatternRegistry(Model):
    patterns: list[NamedPattern] = []
    _index: dict[str, NamedPattern] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # initialize index
        for pattern in self.patterns:
            self._index[pattern.name] = pattern

    def __getitem__(self, name: str) -> NamedPattern:
        return self._index[name]

