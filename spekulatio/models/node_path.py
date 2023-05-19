
from pathlib import Path

from spekulatio.errors import SpekulatioInternalError

def NodePath(path: Path) -> str:
    path_str = str(path)
    if path_str.startswith("/"):
        raise SpekulatioInternalError(f"Nodes are expected to be created from relative paths, received '{path_str}'")
    return "/" if path_str == "." else f"/{path_str}"
