import os
import subprocess
import platform
from collections import defaultdict
from pathlib import Path
from collections.abc import Buffer
from typing import IO, Any, Union, Optional

_default_apps = defaultdict(lambda: ["vi"])
_default_apps["windows"] = ["start", "notepad"]
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

def open(filename: Union[str, Path]="", text: Optional[str]=None, temp: bool=False, editor: Optional[str]=None, pipe=None, *args: str) -> str:
    path = Path(filename) if isinstance(filename, str) else filename
    if filename is not None and Path(filename).exists() and temp:
        raise ValueError("Opened file cannot be temporary if it exists")
    
    process = None
    try:
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()

        args_arr = [*_default_args(), *args, filename] if editor is None else [editor, *args, filename]
        if text is not None:
            path.write_text(text)

        if pipe is not None:
            process = subprocess.Popen(args_arr, stdin=pipe, shell=True)
        else:
            process = subprocess.Popen(args_arr, shell=True)

        return path.read_text()
    finally:
        if temp and path.exists():
            process.terminate()
            process.wait()
            path.unlink()