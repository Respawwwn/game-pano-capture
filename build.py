#!/usr/bin/env python3
"""Build script for creating standalone executable."""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def clean_build():
    """Clean previous build artifacts."""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}/")


def build_executable():
    """Build the executable using PyInstaller."""
    print(f"Building for {platform.system()}...")

    # Run PyInstaller
    cmd = ["pyinstaller", "pano-capture.spec"]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print("Executable created in: dist/")

        # Show the created file
        dist_dir = Path("dist")
        if dist_dir.exists():
            files = list(dist_dir.iterdir())
            for file in files:
                print(f"  - {file.name} ({file.stat().st_size // 1024} KB)")

    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)


def main():
    """Main build process."""
    print("Game Pano Capture - Build Script")
    print("=" * 40)

    # Check if PyInstaller is installed
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: PyInstaller not found. Install with:")
        print("  pip install -r requirements-dev.txt")
        sys.exit(1)

    clean_build()
    build_executable()

    print("\nBuild complete!")
    print("\nTo test the executable:")

    if platform.system() == "Windows":
        print("  .\\dist\\pano-capture.exe --help")
    else:
        print("  ./dist/pano-capture --help")


if __name__ == "__main__":
    main()
