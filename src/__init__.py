"""
Driver Drowsiness Detection System
==================================

A comprehensive computer vision system for detecting driver drowsiness
using real-time eye monitoring and multiple detection algorithms.

Author: Based on original work by Syed Sadi
Enhanced by: [Your Name]
Date: 2025
"""

__version__ = "2.0.0"
__author__ = "Based on original work by Syed Sadi, Enhanced by [Your Name]"
__description__ = "Real-time driver drowsiness detection using computer vision"

from .drowsiness_detector import DrowsinessDetector
from .config import *
from .utils import *

__all__ = [
    'DrowsinessDetector',
    'create_directories',
    'apply_preprocessing',
    'calculate_fps',
    'draw_text_with_background',
    'save_screenshot',
    'validate_cascade_file',
    'get_roi_coordinates',
    'normalize_coordinates',
    'create_alert_overlay'
]
