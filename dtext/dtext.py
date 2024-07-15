import os
import subprocess
import platform
from collections import defaultdict
from pathlib import Path
from typing import Union, Optional

_default_apps = defaultdict(lambda: ["vi"])
_default_apps["windows"] = ["notepad"]
_default_apps["darwin"] = ["open", "-e"]
_default_apps["ubuntu"] = ["gedit"]
_default_apps["fedora"] = ["nano"]

def _default_args() -> list[str]:
    ret = os.getenv("VISUAL", os.getenv("EDITOR", None))

    if ret is None:
        if platform.system() == "Linux":
            import distro
            id = distro.id().lower()
        else:
            id = platform.system().lower()    

        ret = _default_apps[id]

    return ret if isinstance(ret, list) else [ret]

def default() -> str:
    return _default_args()[0]

def open(filename: Union[str, Path]="", text: Union[str, subprocess.ReadableBuffer]="", editor: Optional[str]=None, pipe: Union[subprocess._FILE, subprocess.ReadableBuffer, None]=None, temp: bool=False, *args: str) -> str:
    path = Path(filename) if isinstance(filename, str) else filename
    if filename is not None and Path(filename).exists() and temp:
        raise ValueError("Opened file cannot be temporary if it exists")

    try:
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()

        args_arr = [*_default_args(), *args, filename] if editor is not None else [editor, *args, filename]

        if isinstance(text, str):
            path.write_text(text)
        else:
            path.write_bytes(text)

        match type(pipe):
            case subprocess._FILE:
                subprocess.run(args_arr, check=True, stdin=pipe)
            case subprocess.ReadableBuffer:
                subprocess.run(args_arr, check=True, input=pipe)
            case None:
                subprocess.run(args_arr, check=True)

        return path.read_text()
    finally:
        if temp:
            path.unlink()