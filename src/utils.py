"""
Utility functions for the Drowsiness Detection System
===================================================

This module contains helper functions used throughout the system.
"""

import cv2
import numpy as np
import os
import time
from typing import Tuple, Optional, List
import logging

logger = logging.getLogger(__name__)


def create_directories(paths: List[str]) -> None:
    """
    Create directories if they don't exist.
    
    Args:
        paths: List of directory paths to create
    """
    for path in paths:
        os.makedirs(path, exist_ok=True)


def resize_frame(frame: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    Resize frame to specified dimensions.
    
    Args:
        frame: Input frame
        width: Target width
        height: Target height
        
    Returns:
        Resized frame
    """
    return cv2.resize(frame, (width, height))


def apply_preprocessing(frame: np.ndarray, 
                      enable_median_blur: bool = True,
                      median_kernel_size: int = 5,
                      enable_gaussian_blur: bool = False,
                      gaussian_kernel_size: Tuple[int, int] = (5, 5)) -> np.ndarray:
    """
    Apply preprocessing filters to the frame.
    
    Args:
        frame: Input frame
        enable_median_blur: Whether to apply median blur
        median_kernel_size: Kernel size for median blur
        enable_gaussian_blur: Whether to apply Gaussian blur
        gaussian_kernel_size: Kernel size for Gaussian blur
        
    Returns:
        Preprocessed frame
    """
    processed_frame = frame.copy()
    
    if enable_median_blur:
        processed_frame = cv2.medianBlur(processed_frame, median_kernel_size)
    
    if enable_gaussian_blur:
        processed_frame = cv2.GaussianBlur(processed_frame, gaussian_kernel_size, 0)
    
    return processed_frame


def calculate_fps(frame_count: int, start_time: float) -> Tuple[int, float]:
    """
    Calculate current FPS.
    
    Args:
        frame_count: Number of frames processed
        start_time: Start time for FPS calculation
        
    Returns:
        Tuple of (fps, new_start_time)
    """
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    if elapsed_time >= 1.0:
        fps = int(frame_count / elapsed_time)
        return fps, current_time
    
    return 0, start_time


def draw_text_with_background(img: np.ndarray, text: str, position: Tuple[int, int],
                            font: int, font_scale: float, color: Tuple[int, int, int],
                            thickness: int = 2, bg_color: Tuple[int, int, int] = (0, 0, 0)) -> None:
    """
    Draw text with a background rectangle for better visibility.
    
    Args:
        img: Image to draw on
        text: Text to draw
        position: (x, y) position for text
        font: Font type
        font_scale: Font scale
        color: Text color
        thickness: Text thickness
        bg_color: Background color
    """
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Draw background rectangle
    cv2.rectangle(img, 
                  (position[0], position[1] - text_height - baseline),
                  (position[0] + text_width, position[1] + baseline),
                  bg_color, -1)
    
    # Draw text
    cv2.putText(img, text, position, font, font_scale, color, thickness)


def save_screenshot(frame: np.ndarray, directory: str, prefix: str = "screenshot") -> str:
    """
    Save a screenshot with timestamp.
    
    Args:
        frame: Frame to save
        directory: Directory to save in
        prefix: Filename prefix
        
    Returns:
        Path to saved file
    """
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.jpg"
    filepath = os.path.join(directory, filename)
    
    try:
        cv2.imwrite(filepath, frame)
        logger.info(f"Screenshot saved: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Failed to save screenshot: {e}")
        return ""


def validate_cascade_file(filepath: str) -> bool:
    """
    Validate that a cascade file exists and can be loaded.
    
    Args:
        filepath: Path to cascade file
        
    Returns:
        True if valid, False otherwise
    """
    if not os.path.exists(filepath):
        logger.error(f"Cascade file not found: {filepath}")
        return False
    
    # Try to load the cascade
    cascade = cv2.CascadeClassifier(filepath)
    if cascade.empty():
        logger.error(f"Failed to load cascade: {filepath}")
        return False
    
    return True


def get_roi_coordinates(face_coords: Tuple[int, int, int, int], 
                       eye_coords: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    """
    Get ROI coordinates for eye analysis.
    
    Args:
        face_coords: Face coordinates (x, y, w, h)
        eye_coords: Eye coordinates (x, y, w, h)
        
    Returns:
        ROI coordinates (x, y, w, h)
    """
    fx, fy, fw, fh = face_coords
    ex, ey, ew, eh = eye_coords
    
    # Calculate ROI coordinates
    roi_x = fx + ex
    roi_y = fy + ey
    roi_w = ew
    roi_h = eh
    
    return roi_x, roi_y, roi_w, roi_h


def normalize_coordinates(x: int, y: int, width: int, height: int, 
                         frame_width: int, frame_height: int) -> Tuple[float, float]:
    """
    Normalize coordinates to 0-1 range.
    
    Args:
        x, y: Coordinates
        width, height: Object dimensions
        frame_width, frame_height: Frame dimensions
        
    Returns:
        Normalized coordinates (0-1)
    """
    norm_x = (x + width/2) / frame_width
    norm_y = (y + height/2) / frame_height
    
    return norm_x, norm_y


def create_alert_overlay(frame: np.ndarray, alert_text: str, 
                        alert_level: str = "WARNING") -> np.ndarray:
    """
    Create an alert overlay on the frame.
    
    Args:
        frame: Input frame
        alert_text: Text to display
        alert_level: Alert level (WARNING, CRITICAL, etc.)
        
    Returns:
        Frame with alert overlay
    """
    overlay = frame.copy()
    
    # Define colors based on alert level
    if alert_level == "CRITICAL":
        color = (0, 0, 255)  # Red
        bg_color = (0, 0, 0)  # Black
    elif alert_level == "WARNING":
        color = (0, 165, 255)  # Orange
        bg_color = (0, 0, 0)  # Black
    else:
        color = (0, 255, 0)  # Green
        bg_color = (0, 0, 0)  # Black
    
    # Draw alert text
    draw_text_with_background(overlay, alert_text, (10, 90), 
                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3, bg_color)
    
    return overlay
