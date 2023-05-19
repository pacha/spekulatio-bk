from pydantic import validator

from spekulatio import Model
from .transformation import Transformation


class Preset(Model):
    name: str
    transformations: list[Transformation] = []

