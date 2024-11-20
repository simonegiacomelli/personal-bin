#!/usr/bin/env python3

import os
import sys
from datetime import datetime

# Constants
BRIGHTNESS_PATH = "/sys/class/backlight/intel_backlight/brightness"
MAX_BRIGHTNESS_PATH = "/sys/class/backlight/intel_backlight/max_brightness"
LOG_FILE = "/tmp/brightness.log"
STEP = 52

def get_variable(filename):
    """Read and return the content of a file as an integer."""
    with open(filename, "r") as f:
        return int(f.read().strip())

def log_message(message):
    """Write a message to the log file."""
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} - {message}\n")

def main():
    """Main function to handle brightness adjustment."""
    if len(sys.argv) < 2:
        log_message(f"Error: No arguments provided. Args: {sys.argv}")
        return

    event = sys.argv[1].lower()  # ACPI event passed as argument
    current_brightness = get_variable(BRIGHTNESS_PATH)

    if "brightnessup" in event:
        new_brightness = min(current_brightness + STEP, get_variable(MAX_BRIGHTNESS_PATH))
    elif "brightnessdown" in event:
        new_brightness = max(current_brightness - STEP, 0)
    else:
        log_message(f"Error: Unknown event '{event}'. Args: {sys.argv}")
        return

    with open(BRIGHTNESS_PATH, "w") as f:
        f.write(str(new_brightness))

    log_message(
        f"Event-x: {event}, Current: {current_brightness}, New: {new_brightness}, Args: {sys.argv}"
    )

if __name__ == "__main__":
    main()
