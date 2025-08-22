"""
Configuration file for the Drowsiness Detection System
====================================================

This file contains all configurable parameters for the system.
"""

# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS_TARGET = 30

# Detection parameters
FACE_SCALE_FACTOR = 1.1
FACE_MIN_NEIGHBORS = 5
FACE_MIN_SIZE = (30, 30)

EYE_SCALE_FACTOR = 1.1
EYE_MIN_NEIGHBORS = 5
EYE_MIN_SIZE = (20, 20)

# Eye analysis parameters
THRESHOLD_VALUE = 50
BLACK_PIXELS_MIN = 100
CANNY_LOW_THRESHOLD = 100
CANNY_HIGH_THRESHOLD = 200
EDGE_PIXELS_MIN = 30
EAR_THRESHOLD = 0.2

# Alert settings
ALERT_THRESHOLD_SECONDS = 4.0
ALERT_SOUND_ENABLED = True
ALERT_SOUND_FILE = "beep.wav"

# UI settings
DISPLAY_FPS = True
DISPLAY_BLINK_COUNT = True
DISPLAY_ALERTS = True
SAVE_SCREENSHOTS = True

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE = "drowsiness_detection.log"

# Performance settings
ENABLE_MEDIAN_BLUR = True
MEDIAN_BLUR_KERNEL_SIZE = 5
ENABLE_GAUSSIAN_BLUR = False
GAUSSIAN_BLUR_KERNEL_SIZE = (5, 5)

# Model paths (relative to project root)
MODEL_PATHS = {
    "face_cascade": "models/haarcascade_frontalface_default.xml",
    "eye_cascade": "models/haarcascade_eye.xml"
}

# Data paths
DATA_PATHS = {
    "screenshots": "data/screenshots",
    "logs": "data/logs",
    "sounds": "data/sounds"
}
