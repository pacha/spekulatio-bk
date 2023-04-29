from pathlib import Path

from pydantic import BaseModel


class ActionParamsSpec(BaseModel):
    class Config:
        extra = "allow"


def action(
    input_path: Path, output_path: Path, action_params: dict, values: dict
) -> None:
    pass
