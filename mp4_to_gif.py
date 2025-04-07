#!/usr/bin/env python3
import subprocess
from pathlib import Path

def convert_mp4_to_gif():
    # Get all mp4 files in current directory
    mp4_files = list(Path('.').glob('*.mp4'))
    
    if not mp4_files:
        print("No MP4 files found in the current directory.")
        return
    
    for mp4_file in mp4_files:
        # Generate output filename (replace .mp4 with .gif)
        gif_file = mp4_file.with_suffix('.gif')
        
        # Construct the ffmpeg command
        ffmpeg_cmd = [
            'ffmpeg', 
            '-i', str(mp4_file), 
            '-vf', 'fps=15,scale=1000:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle', 
            str(gif_file)
        ]
    
        
        # Execute the command
        print(f"Converting {mp4_file} to {gif_file}...")
        try:
            subprocess.run(ffmpeg_cmd, check=True)
            print(f"Successfully converted {mp4_file} to {gif_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {mp4_file}: {e}")

if __name__ == "__main__":
    convert_mp4_to_gif()