#!/usr/bin/env python3
"""
Demo script for the Driver Drowsiness Detection System
=====================================================

This script demonstrates various features and configurations of the system.
"""

import sys
import os
import time
import argparse
import logging

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from drowsiness_detector import DrowsinessDetector
from config import *
from utils import create_directories

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def setup_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        'data/screenshots',
        'data/logs',
        'data/sounds'
    ]
    create_directories(directories)
    logger.info("Directories created successfully")


def demo_basic_detection():
    """Demonstrate basic drowsiness detection."""
    logger.info("Starting basic drowsiness detection demo...")
    
    try:
        detector = DrowsinessDetector(
            camera_index=CAMERA_INDEX,
            alert_threshold=ALERT_THRESHOLD_SECONDS
        )
        detector.run()
    except Exception as e:
        logger.error(f"Demo failed: {e}")


def demo_custom_configuration():
    """Demonstrate custom configuration options."""
    logger.info("Starting custom configuration demo...")
    
    # Custom configuration
    custom_config = {
        'camera_index': 0,
        'alert_threshold': 3.0,  # More sensitive
        'frame_width': 320,      # Lower resolution for performance
        'frame_height': 240
    }
    
    logger.info(f"Custom configuration: {custom_config}")
    
    try:
        detector = DrowsinessDetector(
            camera_index=custom_config['camera_index'],
            alert_threshold=custom_config['alert_threshold']
        )
        
        # Override camera settings
        detector.cap.set(cv2.CAP_PROP_FRAME_WIDTH, custom_config['frame_width'])
        detector.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, custom_config['frame_height'])
        
        logger.info("Custom configuration applied successfully")
        detector.run()
    except Exception as e:
        logger.error(f"Custom demo failed: {e}")


def demo_performance_test():
    """Demonstrate performance testing capabilities."""
    logger.info("Starting performance test demo...")
    
    try:
        detector = DrowsinessDetector()
        
        # Performance test loop
        frame_count = 0
        start_time = time.time()
        test_duration = 10  # seconds
        
        logger.info(f"Running performance test for {test_duration} seconds...")
        
        while time.time() - start_time < test_duration:
            ret, frame = detector.cap.read()
            if not ret:
                continue
            
            # Process frame
            frame = cv2.medianBlur(frame, 5)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces and eyes
            faces, eyes = detector._detect_face_and_eyes(frame, gray)
            
            frame_count += 1
            
            # Display progress
            if frame_count % 30 == 0:  # Every 30 frames
                elapsed = time.time() - start_time
                fps = frame_count / elapsed
                logger.info(f"Processed {frame_count} frames, FPS: {fps:.2f}")
        
        # Final statistics
        total_time = time.time() - start_time
        avg_fps = frame_count / total_time
        logger.info(f"Performance test completed:")
        logger.info(f"  Total frames: {frame_count}")
        logger.info(f"  Total time: {total_time:.2f} seconds")
        logger.info(f"  Average FPS: {avg_fps:.2f}")
        
        detector.cleanup()
        
    except Exception as e:
        logger.error(f"Performance test failed: {e}")


def demo_feature_showcase():
    """Showcase various features of the system."""
    logger.info("Starting feature showcase demo...")
    
    features = [
        "Real-time face detection",
        "Eye localization and tracking",
        "Multiple eye state analysis methods",
        "Configurable alert thresholds",
        "Performance monitoring",
        "Screenshot capture",
        "Audio and visual alerts"
    ]
    
    logger.info("System features:")
    for i, feature in enumerate(features, 1):
        logger.info(f"  {i}. {feature}")
    
    logger.info("\nStarting interactive demo...")
    logger.info("Press 'q' to quit, 's' to save screenshot")
    
    try:
        detector = DrowsinessDetector()
        detector.run()
    except Exception as e:
        logger.error(f"Feature showcase failed: {e}")


def main():
    """Main demo function."""
    parser = argparse.ArgumentParser(description="Driver Drowsiness Detection System Demo")
    parser.add_argument('--demo', choices=['basic', 'custom', 'performance', 'features', 'all'],
                       default='basic', help='Type of demo to run')
    parser.add_argument('--setup', action='store_true', help='Setup directories and dependencies')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("Driver Drowsiness Detection System Demo")
    logger.info("=" * 60)
    
    if args.setup:
        setup_directories()
        return
    
    # Run selected demo
    if args.demo == 'basic':
        demo_basic_detection()
    elif args.demo == 'custom':
        demo_custom_configuration()
    elif args.demo == 'performance':
        demo_performance_test()
    elif args.demo == 'features':
        demo_feature_showcase()
    elif args.demo == 'all':
        logger.info("Running all demos...")
        demo_basic_detection()
        time.sleep(2)
        demo_custom_configuration()
        time.sleep(2)
        demo_performance_test()
        time.sleep(2)
        demo_feature_showcase()
    
    logger.info("Demo completed successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo failed with error: {e}")
        sys.exit(1)
