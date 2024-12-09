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


def mark_last(iterable) -> (any, bool):
    """
    A generator function that takes an iterable and yields (item, is_last)
    where is_last is True only for the last item of the iterable.
    """
    it = iter(iterable)
    try:
        prev = next(it)  # Start by reading the first element
    except StopIteration:
        return

    for item in it:
        yield prev, False  # 'prev' is not the last because we have more items ahead
        prev = item

    yield prev, True


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
