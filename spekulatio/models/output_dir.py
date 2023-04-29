from pathlib import Path
from pydantic import validator

from spekulatio import Model


class OutputDir(Model):
    root_path: Path
    path: Path

    @validator("path", pre=True)
    def check_path(cls, value, values):
        path = Path(value) if isinstance(value, str) else value
        absolute_path = values["root_path"] / path
        if not absolute_path.is_dir():
            raise ValueError(f"Can't find output directory '{ path }'.")
        return absolute_path

    @property
    def absolute_path(self) -> Path:
        return self.root_path / self.path
