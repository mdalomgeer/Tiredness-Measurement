#!/usr/bin/env python3
"""
Test suite for the Drowsiness Detection System
==============================================

This module contains tests to verify the system functionality.
"""

import unittest
import sys
import os
import numpy as np
import cv2

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from drowsiness_detector import DrowsinessDetector
from utils import apply_preprocessing, calculate_fps, draw_text_with_background


class TestDrowsinessDetector(unittest.TestCase):
    """Test cases for the DrowsinessDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock camera (we'll use a test image instead)
        self.test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
    def test_preprocessing(self):
        """Test image preprocessing functions."""
        # Test median blur
        processed = apply_preprocessing(self.test_image, enable_median_blur=True)
        self.assertIsInstance(processed, np.ndarray)
        self.assertEqual(processed.shape, self.test_image.shape)
        
        # Test Gaussian blur
        processed = apply_preprocessing(self.test_image, enable_gaussian_blur=True)
        self.assertIsInstance(processed, np.ndarray)
        self.assertEqual(processed.shape, self.test_image.shape)
    
    def test_fps_calculation(self):
        """Test FPS calculation."""
        fps, new_start_time = calculate_fps(30, 0.0)
        self.assertIsInstance(fps, int)
        self.assertIsInstance(new_start_time, float)
    
    def test_text_drawing(self):
        """Test text drawing with background."""
        test_img = np.zeros((100, 200, 3), dtype=np.uint8)
        draw_text_with_background(test_img, "Test", (10, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
        
        # Check if image was modified
        self.assertFalse(np.array_equal(test_img, np.zeros((100, 200, 3), dtype=np.uint8)))
    
    def test_cascade_loading(self):
        """Test cascade file loading."""
        # This test requires the cascade files to be present
        cascade_path = os.path.join(os.path.dirname(__file__), '..', 'models', 
                                   'haarcascade_frontalface_default.xml')
        
        if os.path.exists(cascade_path):
            cascade = cv2.CascadeClassifier(cascade_path)
            self.assertFalse(cascade.empty())
        else:
            self.skipTest("Cascade files not available")
    
    def test_image_operations(self):
        """Test basic image operations."""
        # Test grayscale conversion
        gray = cv2.cvtColor(self.test_image, cv2.COLOR_BGR2GRAY)
        self.assertEqual(len(gray.shape), 2)
        self.assertEqual(gray.shape[:2], self.test_image.shape[:2])
        
        # Test thresholding
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        self.assertEqual(thresh.shape, gray.shape)
        
        # Test Canny edge detection
        edges = cv2.Canny(gray, 100, 200)
        self.assertEqual(edges.shape, gray.shape)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_directory_creation(self):
        """Test directory creation utility."""
        from utils import create_directories
        
        test_dir = "test_temp_dir"
        create_directories([test_dir])
        
        self.assertTrue(os.path.exists(test_dir))
        
        # Cleanup
        os.rmdir(test_dir)
    
    def test_coordinate_operations(self):
        """Test coordinate utility functions."""
        from utils import get_roi_coordinates, normalize_coordinates
        
        # Test ROI coordinates
        face_coords = (100, 100, 200, 200)
        eye_coords = (50, 50, 100, 100)
        roi_coords = get_roi_coordinates(face_coords, eye_coords)
        
        self.assertEqual(roi_coords, (150, 150, 100, 100))
        
        # Test coordinate normalization
        norm_coords = normalize_coordinates(100, 100, 200, 200, 640, 480)
        self.assertIsInstance(norm_coords[0], float)
        self.assertIsInstance(norm_coords[1], float)
        self.assertTrue(0 <= norm_coords[0] <= 1)
        self.assertTrue(0 <= norm_coords[1] <= 1)


def run_tests():
    """Run all tests."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestDrowsinessDetector))
    test_suite.addTest(unittest.makeSuite(TestUtils))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
