from pathlib import Path
from typing import Generator
from pydantic import validator

from spekulatio import Model
from spekulatio.registry import obj_registry
from spekulatio.lib.traverse_dir import traverse_dir
from .preset import Preset
from .transformation import Transformation


class InputDir(Model):
    root_path: Path
    path: Path
    preset: Preset | None
    transformations: list[Transformation] = []

    @validator("path", pre=True)
    def check_path(cls, value, values):
        path = Path(value) if isinstance(value, str) else value
        absolute_path = values["root_path"] / path
        if not absolute_path.is_dir():
            raise ValueError(f"Can't find input directory '{ path }'.")
        return absolute_path

    @validator("preset", pre=True)
    def check_preset(cls, value):
        if isinstance(value, str):
            try:
                preset = obj_registry[Preset][value]
            except KeyError:
                raise ValueError(f"Named preset '{ value }' doesn't exist.")
        else:
            preset = value
        return preset

    @property
    def absolute_path(self) -> Path:
        return self.root_path / self.path

    def get_transformation(self, path: Path):
        for transformation in self.transformations:
            if transformation.pattern.match(path):
                return transformation
        return None

    def __iter__(self) -> Generator[Path, None, None]:  # type: ignore
        for relative_path in traverse_dir(self.absolute_path):
            yield relative_path

    def __str__(self):
        return str(self.absolute_path)
