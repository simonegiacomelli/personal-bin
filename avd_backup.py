#!/usr/bin/env python3
"""
Android AVD Configuration Backup/Restore Tool
Backs up and restores AVD configuration files (not data)
"""

import os
import sys
import zipfile
import argparse
from pathlib import Path


def get_avd_dir():
    """Get the AVD directory path"""
    return Path.home() / ".android" / "avd"


def list_avds():
    """List all available AVDs"""
    avd_dir = get_avd_dir()
    
    if not avd_dir.exists():
        print(f"❌ AVD directory not found: {avd_dir}")
        return []
    
    # Find all .ini files (excluding hardware-qemu.ini and others inside .avd folders)
    ini_files = [f for f in avd_dir.glob("*.ini") 
                 if not f.name.startswith("hardware-")]
    
    avds = []
    for ini_file in ini_files:
        avd_name = ini_file.stem  # filename without extension
        avd_folder = avd_dir / f"{avd_name}.avd"
        
        if avd_folder.exists():
            config_file = avd_folder / "config.ini"
            if config_file.exists():
                avds.append({
                    'name': avd_name,
                    'ini_file': ini_file,
                    'avd_folder': avd_folder,
                    'config_file': config_file
                })
    
    return avds


def print_avd_info(config_file):
    """Print relevant info from config.ini"""
    if not config_file.exists():
        return

    # Read config file as plain text (no section headers)
    config_data = {}
    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                config_data[key.strip()] = value.strip()

    interesting_keys = {
        'hw.lcd.width': 'Width',
        'hw.lcd.height': 'Height',
        'hw.lcd.density': 'DPI',
        'hw.ramSize': 'RAM',
        'image.sysdir.1': 'System Image',
        'hw.keyboard': 'Hardware Keyboard',
        'skin.name': 'Skin',
    }

    print("  Configuration:")
    for key, label in interesting_keys.items():
        if key in config_data:
            print(f"    • {label}: {config_data[key]}")


def backup_avd(avd_info, output_path):
    """Backup AVD configuration to a zip file"""
    print(f"\n📦 Backing up AVD: {avd_info['name']}")
    print(f"   From: {get_avd_dir()}")
    print(f"   To: {output_path}")
    
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add the .ini file
            arcname = avd_info['ini_file'].name
            zipf.write(avd_info['ini_file'], arcname)
            print(f"   ✓ Added {arcname}")
            
            # Add the config.ini from the .avd folder
            arcname = f"{avd_info['name']}.avd/config.ini"
            zipf.write(avd_info['config_file'], arcname)
            print(f"   ✓ Added {arcname}")
            
            # Add hardware-qemu.ini if it exists
            hw_qemu = avd_info['avd_folder'] / "hardware-qemu.ini"
            if hw_qemu.exists():
                arcname = f"{avd_info['name']}.avd/hardware-qemu.ini"
                zipf.write(hw_qemu, arcname)
                print(f"   ✓ Added {arcname}")
        
        print(f"\n✅ Backup completed successfully!")
        print(f"   File: {output_path}")
        print(f"   Size: {os.path.getsize(output_path)} bytes")
        
    except Exception as e:
        print(f"\n❌ Backup failed: {e}")
        sys.exit(1)


def restore_avd(zip_path):
    """Restore AVD configuration from a zip file"""
    zip_path = Path(zip_path).expanduser()
    
    if not zip_path.exists():
        print(f"❌ Backup file not found: {zip_path}")
        sys.exit(1)
    
    print(f"\n📋 Analyzing backup file: {zip_path}")
    
    avd_dir = get_avd_dir()
    
    # Read the zip file to see what's inside
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            files = zipf.namelist()
            
            # Find the AVD name from the .ini file
            ini_files = [f for f in files if f.endswith('.ini') and '/' not in f]
            if not ini_files:
                print("❌ No AVD .ini file found in backup")
                sys.exit(1)
            
            avd_name = Path(ini_files[0]).stem
            
            print(f"\n📦 Backup contains AVD: {avd_name}")
            print(f"\n📁 Files in backup:")
            for f in files:
                print(f"   • {f}")
            
            # Show where files will be written
            print(f"\n📝 Will restore to:")
            print(f"   Target directory: {avd_dir}")
            print(f"\n   Files to be created/overwritten:")
            for f in files:
                target = avd_dir / f
                status = "⚠️  EXISTS - will overwrite" if target.exists() else "✓ new file"
                print(f"   • {target}")
                print(f"     {status}")
            
            # Show config preview if available
            config_file = f"{avd_name}.avd/config.ini"
            if config_file in files:
                print(f"\n⚙️  Configuration preview:")
                config_content = zipf.read(config_file).decode('utf-8')

                # Parse config as plain text (no section headers)
                config_data = {}
                for line in config_content.splitlines():
                    line = line.strip()
                    if line and '=' in line:
                        key, value = line.split('=', 1)
                        config_data[key.strip()] = value.strip()

                interesting_keys = {
                    'hw.lcd.width': 'Width',
                    'hw.lcd.height': 'Height',
                    'hw.lcd.density': 'DPI',
                    'hw.ramSize': 'RAM',
                    'image.sysdir.1': 'System Image',
                }

                for key, label in interesting_keys.items():
                    if key in config_data:
                        print(f"   • {label}: {config_data[key]}")
            
            # Ask for confirmation
            print(f"\n{'='*60}")
            response = input("\n⚠️  Proceed with restore? (yes/no): ").strip().lower()
            
            if response not in ['yes', 'y']:
                print("❌ Restore cancelled")
                sys.exit(0)
            
            # Perform restore
            print(f"\n🔄 Restoring...")
            
            # Create AVD directory if it doesn't exist
            avd_folder = avd_dir / f"{avd_name}.avd"
            avd_folder.mkdir(parents=True, exist_ok=True)
            
            for f in files:
                target = avd_dir / f
                target.parent.mkdir(parents=True, exist_ok=True)
                
                with open(target, 'wb') as out_file:
                    out_file.write(zipf.read(f))
                print(f"   ✓ Restored {f}")
            
            print(f"\n✅ Restore completed successfully!")
            print(f"   AVD '{avd_name}' should now be available in Android Studio")
            print(f"\n💡 Note: You may need to download the system image if not already installed")
            
    except Exception as e:
        print(f"\n❌ Restore failed: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Backup and restore Android AVD configurations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Backup an AVD
  %(prog)s
  
  # Restore an AVD
  %(prog)s --restore ~/Downloads/Pixel_5_API_34.zip
        """
    )
    
    parser.add_argument(
        '--restore',
        metavar='ZIP_FILE',
        help='Restore AVD from backup zip file'
    )
    
    args = parser.parse_args()
    
    if args.restore:
        # Restore mode
        restore_avd(args.restore)
    else:
        # Backup mode
        avds = list_avds()
        
        if not avds:
            print("❌ No AVDs found")
            sys.exit(1)
        
        print("📱 Available AVDs:\n")
        for i, avd in enumerate(avds, 1):
            print(f"{i}. {avd['name']}")
            print_avd_info(avd['config_file'])
            print()
        
        # Ask user to select
        while True:
            try:
                choice = input(f"Select AVD to backup (1-{len(avds)}) or 'q' to quit: ").strip()
                
                if choice.lower() == 'q':
                    print("Cancelled")
                    sys.exit(0)
                
                idx = int(choice) - 1
                if 0 <= idx < len(avds):
                    selected_avd = avds[idx]
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(avds)}")
            except ValueError:
                print("❌ Please enter a valid number")
        
        # Ask for output path
        default_output = Path.home() / "Downloads" / f"{selected_avd['name']}.zip"
        output_input = input(f"\nBackup location [{default_output}]: ").strip()
        
        output_path = Path(output_input).expanduser() if output_input else default_output
        
        # Create parent directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists
        if output_path.exists():
            response = input(f"⚠️  File exists. Overwrite? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("Cancelled")
                sys.exit(0)
        
        # Perform backup
        backup_avd(selected_avd, output_path)


if __name__ == "__main__":
    main()
