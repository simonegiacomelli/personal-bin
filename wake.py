#!/usr/bin/env python3
import socket
import sys
from pathlib import Path


def wake_on_lan(mac: str, interface: str = None):
    mac_no_sep = mac.replace(':', '').replace('-', '')
    if len(mac_no_sep) != 12:
        print(f'Invalid mac: {mac}')
    packet = bytes.fromhex("F" * 12 + mac_no_sep * 16)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        if interface is not None:
            sock.bind((interface, 0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.connect(('255.255.255.255', 9))
        sock.send(packet)


def main():
    if len(sys.argv) != 2:
        print('Please, specify a hostname or a mac to wake')
        exit(1)

    hostname = sys.argv[1]

    prop_file = Path(__file__).parent / 'personal-bin-config/wakeonlan.properties'
    text = prop_file.read_text()
    props = text_to_props(text)

    mac = props.get(f'host.{hostname}', None)
    if mac is None:
        print(f'Configuration key `{hostname}` not found in `{prop_file}`')
        exit(2)
    wake_on_lan(mac)


def text_to_props(text):
    lines = text.splitlines(keepends=False)
    # remove blank lines
    lines = [line for line in lines if line.strip()]
    props = dict([v.split('=', maxsplit=1) for v in lines])
    return props


if __name__ == '__main__':
    main()
