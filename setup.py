import platform
import subprocess
import os
from pathlib import Path

def install_requirements():
    """Install the appropriate requirements based on the operating system."""

    # Get the current operating system
    system = platform.system().lower()

    # Get the directory containing this script
    base_dir = Path(__file__).parent
    req_dir = base_dir / 'requirements'

    # Map OS to requirements file
    requirements_map = {
        'windows': 'windows.txt',
        'darwin': 'macos.txt',
        'linux': 'linux.txt'
    }

    # Get the appropriate requirements file
    req_file = requirements_map.get(system, 'base.txt')
    req_path = req_dir / req_file

    print(f"Installing requirements for {system.title()}...")

    try:
        # Install requirements using pip
        subprocess.check_call([
            'pip', 'install', '-r', str(req_path)
        ])
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

    return True

if __name__ == "__main__":
    install_requirements()