from __future__ import annotations

import shlex
import subprocess
from pathlib import Path


def get_video_path() -> Path:
    return Path(subprocess.check_output('xdg-user-dir VIDEOS'.split(' ')).decode().strip())


class Line:
    def __init__(self, line: str):
        self.line = line
        self.ignore = line.lstrip().startswith('#') or line.strip() == ''
        all_args = shlex.split(line) if not self.ignore else []
        self.command = all_args[0] if all_args else ''
        self.args = all_args[1:]


extension = 'irp'
