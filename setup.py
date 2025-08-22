#!/usr/bin/env python3
"""
Setup script for the Driver Drowsiness Detection System
======================================================

This script handles installation, dependency management, and initial setup.
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def print_banner():
    """Print setup banner."""
    print("=" * 60)
    print("Driver Drowsiness Detection System Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    return True

def check_dependencies():
    """Check if required dependencies are available."""
    print("Checking dependencies...")
    
    required_packages = [
        'opencv-python',
        'numpy',
        'pygame'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        return False
    
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\nInstalling dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print("\nCreating directories...")
    
    directories = [
        'data/screenshots',
        'data/logs',
        'data/sounds',
        'models'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")

def download_cascade_files():
    """Download required Haar cascade files."""
    print("\nDownloading Haar cascade files...")
    
    cascade_urls = {
        'haarcascade_frontalface_default.xml': 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml',
        'haarcascade_eye.xml': 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_eye.xml'
    }
    
    import urllib.request
    
    for filename, url in cascade_urls.items():
        filepath = Path('models') / filename
        
        if filepath.exists():
            print(f"✅ {filename} - Already exists")
            continue
        
        try:
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, filepath)
            print(f"✅ Downloaded: {filename}")
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
            return False
    
    return True

def create_sample_config():
    """Create a sample configuration file."""
    print("\nCreating sample configuration...")
    
    config_content = '''# Sample configuration for Drowsiness Detection System
# Copy this file to src/config.py and modify as needed

# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Detection parameters
ALERT_THRESHOLD_SECONDS = 4.0
THRESHOLD_VALUE = 50
BLACK_PIXELS_MIN = 100

# Performance settings
ENABLE_MEDIAN_BLUR = True
MEDIAN_BLUR_KERNEL_SIZE = 5
'''
    
    config_file = Path('src/config_sample.py')
    config_file.write_text(config_content)
    print(f"✅ Created: {config_file}")

def run_tests():
    """Run system tests."""
    print("\nRunning tests...")
    
    try:
        result = subprocess.run([sys.executable, "tests/test_detector.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Tests passed")
            return True
        else:
            print("❌ Tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def print_usage_instructions():
    """Print usage instructions."""
    print("\n" + "=" * 60)
    print("Setup Complete! 🎉")
    print("=" * 60)
    print()
    print("To run the system:")
    print("  python src/drowsiness_detector.py")
    print()
    print("To run the demo:")
    print("  python demo.py")
    print()
    print("To run tests:")
    print("  python tests/test_detector.py")
    print()
    print("For more information, see README.md")
    print()

def main():
    """Main setup function."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\nInstalling missing dependencies...")
        if not install_dependencies():
            print("❌ Setup failed!")
            return
    
    # Create directories
    create_directories()
    
    # Download cascade files
    if not download_cascade_files():
        print("❌ Setup failed!")
        return
    
    # Create sample config
    create_sample_config()
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but setup completed")
    
    # Print usage instructions
    print_usage_instructions()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)
