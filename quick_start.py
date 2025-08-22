#!/usr/bin/env python3
"""
Quick Start Script for Driver Drowsiness Detection
=================================================

This script provides a quick way to test the system without full setup.
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if basic dependencies are available."""
    try:
        import cv2
        print("✅ OpenCV available")
    except ImportError:
        print("❌ OpenCV not available. Install with: pip install opencv-python")
        return False
    
    try:
        import numpy
        print("✅ NumPy available")
    except ImportError:
        print("❌ NumPy not available. Install with: pip install numpy")
        return False
    
    return True

def quick_test():
    """Run a quick test of the system."""
    print("🚀 Running quick test...")
    
    try:
        import cv2
        
        # Test camera access
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera access successful")
            ret, frame = cap.read()
            if ret:
                print(f"✅ Frame captured: {frame.shape}")
            else:
                print("⚠️  Could not read frame")
            cap.release()
        else:
            print("❌ Camera access failed")
            return False
        
        # Test cascade loading
        cascade_path = "models/haarcascade_frontalface_default.xml"
        if os.path.exists(cascade_path):
            cascade = cv2.CascadeClassifier(cascade_path)
            if not cascade.empty():
                print("✅ Face cascade loaded successfully")
            else:
                print("❌ Face cascade loading failed")
                return False
        else:
            print("❌ Face cascade file not found")
            return False
        
        print("🎉 Quick test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

def main():
    """Main quick start function."""
    print("=" * 50)
    print("Driver Drowsiness Detection - Quick Start")
    print("=" * 50)
    
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        return
    
    print("\nRunning system check...")
    if quick_test():
        print("\n✅ System is ready!")
        print("\nTo run the full system:")
        print("  python src/drowsiness_detector.py")
        print("\nTo run the demo:")
        print("  python demo.py")
        print("\nTo run tests:")
        print("  python tests/test_detector.py")
    else:
        print("\n❌ System check failed. Please check the errors above.")

if __name__ == "__main__":
    main()
