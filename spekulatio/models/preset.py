from pydantic import validator

from spekulatio import Model
from spekulatio.registry import obj_registry
from .transformation import Transformation


class Preset(Model):
    name: str
    transformations: list[Transformation] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # register globally
        obj_registry[self.__class__][self.name] = self
