from spekulatio.registry import obj_registry
from . import Pattern


class NamedPattern(Pattern):
    name: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # register globally
        obj_registry[self.__class__][self.name] = self
