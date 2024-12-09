from __future__ import annotations

import json
import random
import shlex
import subprocess
from pathlib import Path
from time import sleep


def get_video_path() -> Path:
    return Path(subprocess.check_output('xdg-user-dir VIDEOS'.split(' ')).decode().strip())


class Line:
    def __init__(self, line: str):
        self.line = line
        self.ignore = line.lstrip().startswith('#') or line.strip() == ''
        all_args = shlex.split(line) if not self.ignore else []
        self.command = all_args[0] if all_args else ''
        self.args = all_args[1:]


def text_parse(text):
    dec_text = json.loads(f'"{text}"')
    return dec_text


def human_delay(after_char: str = None):
    normal = (0.08, 0.3)
    long = (0.5, 1.5)
    min_delay, max_delay = normal if after_char != '\n' else long
    delay = abs(random.uniform(min_delay, max_delay))
    return delay


extension = 'irp'


def main():
    text = 'cd $(mktemp -d demo-XXX)'
    for c in text:
        print(c, end='', flush=True)
        delay = human_delay(c)
        sleep(delay)
    print()


if __name__ == '__main__':
    main()
