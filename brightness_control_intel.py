#!/usr/bin/env python3
import math
import sys
from datetime import datetime
from pathlib import Path

BACKLIGHT_PATH = Path("/sys/class/backlight/intel_backlight")


def get_variable(filename):
    return int(Path(BACKLIGHT_PATH / filename).read_text().strip())


def set_variable(filename, value):
    Path(BACKLIGHT_PATH / filename).write_text(str(value))


def log(message):
    with open('/tmp/brightness.log', "a") as log:
        log.write(f"{datetime.now()} - {message}\n")


def main():
    if len(sys.argv) < 2:
        log(f"Error: No arguments provided. Args: {sys.argv}")
        return

    event = sys.argv[1].lower()  # ACPI event passed as argument
    current_brightness = get_variable('brightness')
    max_brightness = get_variable('max_brightness')
    step_count = 20
    step = math.ceil(max_brightness / step_count)

    if "brightnessup" in event:
        new_brightness = min(current_brightness + step, max_brightness)
    elif "brightnessdown" in event:
        new_brightness = max(current_brightness - step, 0)
    else:
        log(f"Error: Unknown event '{event}'. Args: {sys.argv}")
        return

    set_variable('brightness', new_brightness)

    log(f"Event: {event}, Current: {current_brightness}, New: {new_brightness}, "
        f"max: {max_brightness} step-count: {step_count}, step: {step}")



if __name__ == "__main__":
    main()
