#!/usr/bin/env python3
import sys
from enum import Enum
from os.path import expanduser
from pathlib import Path


class Status(Enum):
    ACTIVE = 'A'
    COMMENTED = 'C'
    MISSING = 'M'


_marker = '-Dsun.java2d.uiScale='
_option = '-Dsun.java2d.uiScale=2'


def status(content: str) -> Status:
    if _marker not in content:
        return Status.MISSING

    lines = content.split('\n')
    for line in lines:
        if _marker not in line:
            continue
        if line.strip().startswith('#'):
            return Status.COMMENTED
        else:
            return Status.ACTIVE

    assert 'whhaaat' == 'success'


def activate(content: str) -> str:
    return update(content, Status.ACTIVE)


def comment(content: str) -> str:
    return update(content, Status.COMMENTED)


def remove(content: str) -> str:
    return update(content, Status.MISSING)


def update(content: str, new: Status) -> str:
    old = status(content)
    if old == new:
        return content

    lines = content.split('\n')
    index = -1
    for i, line in enumerate(lines):
        if _marker in line:
            index = i
            break

    if index == -1:
        index = len(lines)
        lines.append('')

    if new == Status.MISSING:
        del lines[index]
    elif new == Status.ACTIVE:
        lines[index] = _option
    elif new == Status.COMMENTED:
        lines[index] = '#' + _option
    else:
        assert 'unexpected' == 'state'

    return '\n'.join(lines)
