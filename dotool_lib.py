import subprocess
import sys
from pathlib import Path


class DotoolKeys:
    def __init__(self):
        self.content = Path(__file__).parent / 'dotool_keys.txt'
        self.keys = set()
        for line in self.content.read_text().splitlines(keepends=False):
            key = line.split()[0]
            self.keys.add(key)

class DotoolKeyboard:

    def __init__(self):
        self.process = subprocess.Popen(['dotool'], stdin=subprocess.PIPE, text=True)
        self.dotool_keys = DotoolKeys()

    def send(self, dotool_command: str):
        # print(f'dotool: {line}')
        self.process.stdin.write(f'{dotool_command}\n')
        self.process.stdin.flush()

    def type_char(self, char: str):
        mapping = {
            '\n': 'enter',
            '\t': 'tab',
            '\b': 'backspace',
            '\x1b': 'esc',
            '\x7f': 'delete',
        }
        special = mapping.get(char, None)
        if special:
            self.send(f'key {special}')
            print(special, end='')
        else:
            self.send(f'type {char}')
            print(char, end='')

    def has_chord(self, key: str):
        return key in self.dotool_keys.keys

    def exit_if_unrecognized(self, key: str):
        if not self.has_chord(key):
            print(f'unknown key: {key}')
            sys.exit(1)
