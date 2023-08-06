import os
from pathlib import Path
import pipes
from typing import Union

PathOrStr = Union[Path, str]


def to_path(path: PathOrStr, expanduser=True) -> Path:
    if type(path) == str:
        if expanduser:
            path = os.path.expanduser(path)
        return Path(path)
    else:
        return path


def quote_path(path: Path) -> str:
    return pipes.quote(str(path))
