from __future__ import annotations

import json
import random
import shlex
import subprocess
from pathlib import Path
from time import sleep
from typing import NamedTuple


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
    dec_text = json.loads(text)
    return dec_text


class HumanDelay(NamedTuple):
    normal_char: (float, float)
    long_char: (float, float)


default_delay = HumanDelay((0.08, 0.3), (0.5, 1.5))


def human_delay(after_char: str = None, delay: HumanDelay = default_delay) -> float:
    d = delay.long_char if after_char == '\n' else delay.normal_char
    return abs(random.uniform(*d))


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


class Human:
    def __init__(self, dotool, stop_replay: callable):
        self.dotool = dotool
        self.stop_replay = stop_replay
        self.delay = default_delay

    def type(self, text):
        """:text: will be wrapped with double quote and decoded as json"""
        dec_text = text_parse(text)
        for char in dec_text:
            if self.stop_replay():
                break
            self.dotool.type_char(char)
            sleep(human_delay(char, self.delay))

    def process_line(self, line: Line):
        args = line.args
        cmd = args[0]
        if cmd == 'type':
            text = line.line.split(' ', 2)[2]
            self.type(text)
        elif cmd == 'delay':
            if args[1] == 'default':
                self.delay = default_delay
            elif args[1] == 'fast':
                self.delay = HumanDelay((0, 0), (0.3, 0.3))
            else:
                raise Exception(f'unknown delay: {args[1]} ~~ {line.line}')
        else:
            print(f'unknown command: {line.line}')


extension = 'cfg'


class SmartSeparator:

    def __init__(self):
        self.tuple = ('', '')
        self._last = None

    def process(self, command: str):
        same = command == self._last
        if same:
            self.tuple = ('\t', '')
        else:
            if self._last:
                self.tuple = ('\n', '')

        self._last = command
        return self.tuple
