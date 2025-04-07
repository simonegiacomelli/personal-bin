#!/usr/bin/env python3

import subprocess
import datetime
import os
from pathlib import Path

# Get current timestamp formatted as yyyy-mm-dd_hh-MM-ss
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create the full path for the output file
output_filename = f"Clipboard_{timestamp}.png"
pictures_dir = os.path.expanduser("~/Pictures")
output_path = os.path.join(pictures_dir, output_filename)

# Make sure the Pictures directory exists
Path(pictures_dir).mkdir(exist_ok=True)

# Run the xclip command and save output to the file
try:
    with open(output_path, 'wb') as f:
        result = subprocess.run(
            ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-o'],
            stdout=f,
            check=True
        )
    print(f"Image saved to: {output_path}")
except subprocess.CalledProcessError:
    print("Error: Failed to get image from clipboard. Is there an image copied?")
except Exception as e:
    print(f"Error: {e}")