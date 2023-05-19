from pathlib import Path
from typing import Generator
from pydantic import validator

from spekulatio import Model
from spekulatio.lib.traverse_dir import traverse_dir
from . import Preset
from . import Transformation
from . import PresetRegistry
from . import PatternRegistry


class InputDir(Model):
    root_path: Path
    pattern_registry: PatternRegistry = PatternRegistry()
    path: Path
    preset_registry: PresetRegistry = PresetRegistry()
    preset: Preset | None
    transformations: list[Transformation] = []
    value_files: list[list[str]] = [
        ["_values.yaml", "_values.yml", "_values.json", "_values.py", "_values"],
        [
            "_values-override.yaml",
            "_values-override.yml",
            "_values-override.json",
            "_values-override.py",
            "_values-override",
        ],
    ]

    @validator("path", pre=True)
    def check_path(cls, value, values):
        path = Path(value) if isinstance(value, str) else value
        absolute_path = values["root_path"] / path
        if not absolute_path.is_dir():
            raise ValueError(f"Can't find input directory '{ path }'.")
        return absolute_path

    @validator("preset", pre=True)
    def check_preset(cls, value, values):
        preset_registry = values['preset_registry']
        if isinstance(value, str):
            try:
                preset = preset_registry[value]
            except KeyError:
                raise ValueError(f"Named preset '{ value }' doesn't exist.")
        else:
            preset = value
        return preset

    @validator("transformations", pre=True)
    def check_transformations(cls, value, values):
        try:
            for transformation in value:
                transformation['pattern_registry'] = values['pattern_registry']
        except Exception:
            raise ValueError("'transformation' must be a dictionary of values.")
        return value

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
