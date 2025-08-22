#!/usr/bin/env python3
"""
Driver Drowsiness Detection System
==================================

This program detects driver drowsiness by monitoring eye blinks using computer vision.
It combines multiple detection methods for improved accuracy and provides real-time alerts.

Author: Based on original work by Syed Sadi
Enhanced by: [Your Name]
Date: 2025
"""

import cv2
import numpy as np
import time
import pygame
import os
import sys
from typing import Tuple, Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DrowsinessDetector:
    """
    Main class for drowsiness detection using computer vision.
    """
    
    def __init__(self, camera_index: int = 0, alert_threshold: float = 4.0):
        """
        Initialize the drowsiness detector.
        
        Args:
            camera_index: Index of the camera to use
            alert_threshold: Time threshold (seconds) before triggering alert
        """
        self.camera_index = camera_index
        self.alert_threshold = alert_threshold
        
        # Initialize camera
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera at index {camera_index}")
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Load Haar cascade classifiers
        self.face_cascade = self._load_cascade('haarcascade_frontalface_default.xml')
        self.eye_cascade = self._load_cascade('haarcascade_eye.xml')
        
        # Initialize pygame mixer for alerts
        pygame.mixer.init()
        self.alert_sound = self._load_alert_sound()
        
        # State variables
        self.blink_count = 0
        self.last_blink_time = 0
        self.eyes_closed_start = 0
        self.eyes_closed = False
        
        # Performance metrics
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
        logger.info("Drowsiness detector initialized successfully")
    
    def _load_cascade(self, filename: str) -> cv2.CascadeClassifier:
        """Load a Haar cascade classifier from the models directory."""
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', filename)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Cascade file not found: {model_path}")
        
        cascade = cv2.CascadeClassifier(model_path)
        if cascade.empty():
            raise RuntimeError(f"Failed to load cascade: {filename}")
        
        return cascade
    
    def _load_alert_sound(self) -> Optional[pygame.mixer.Sound]:
        """Load alert sound file."""
        try:
            # Try to load a default beep sound
            sound_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'beep.wav')
            if os.path.exists(sound_path):
                return pygame.mixer.Sound(sound_path)
            else:
                logger.warning("Alert sound file not found, alerts will be visual only")
                return None
        except Exception as e:
            logger.warning(f"Could not load alert sound: {e}")
            return None
    
    def _detect_face_and_eyes(self, frame: np.ndarray, gray: np.ndarray) -> Tuple[List, List]:
        """
        Detect faces and eyes in the frame.
        
        Args:
            frame: BGR color frame
            gray: Grayscale frame
            
        Returns:
            Tuple of (faces, eyes) detection results
        """
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        eyes = []
        for (x, y, w, h) in faces:
            # Define region of interest for face (upper half where eyes are)
            roi_gray = gray[y:y + int(h/2), x:x + w]
            roi_color = frame[y:y + int(h/2), x:x + w]
            
            # Detect eyes in the face ROI
            eyes_in_face = self.eye_cascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(20, 20)
            )
            
            # Convert eye coordinates to full frame coordinates
            for (ex, ey, ew, eh) in eyes_in_face:
                eyes.append((x + ex, y + ey, ew, eh))
        
        return faces, eyes
    
    def _analyze_eye_state(self, frame: np.ndarray, gray: np.ndarray, 
                          face: Tuple[int, int, int, int], 
                          eye: Tuple[int, int, int, int]) -> bool:
        """
        Analyze if the eye is open or closed using multiple methods.
        
        Args:
            frame: BGR color frame
            gray: Grayscale frame
            face: Face coordinates (x, y, w, h)
            eye: Eye coordinates (x, y, w, h)
            
        Returns:
            True if eye is open, False if closed
        """
        fx, fy, fw, fh = face
        ex, ey, ew, eh = eye
        
        # Get eye ROI
        eye_roi = gray[ey:ey + eh, ex:ex + ew]
        
        if eye_roi.size == 0:
            return True
        
        # Method 1: Thresholding
        _, thresh_eye = cv2.threshold(eye_roi, 50, 255, cv2.THRESH_BINARY)
        black_pixels = thresh_eye.size - cv2.countNonZero(thresh_eye)
        
        # Method 2: Canny edge detection
        canny_eye = cv2.Canny(eye_roi, 100, 200)
        edge_pixels = cv2.countNonZero(canny_eye)
        
        # Method 3: Eye aspect ratio (EAR)
        ear = self._calculate_eye_aspect_ratio(eye_roi)
        
        # Combine methods for decision
        is_open = (
            black_pixels > 100 and  # Threshold method
            edge_pixels > 30 and    # Canny method
            ear > 0.2               # EAR method
        )
        
        return is_open
    
    def _calculate_eye_aspect_ratio(self, eye_roi: np.ndarray) -> float:
        """Calculate the Eye Aspect Ratio (EAR) for the given eye region."""
        try:
            # Find contours in the eye ROI
            contours, _ = cv2.findContours(eye_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return 0.0
            
            # Get the largest contour (should be the eye)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Calculate the convex hull
            hull = cv2.convexHull(largest_contour)
            
            # Calculate area ratios
            eye_area = cv2.contourArea(largest_contour)
            hull_area = cv2.contourArea(hull)
            
            if hull_area == 0:
                return 0.0
            
            return eye_area / hull_area
        except Exception:
            return 0.0
    
    def _update_fps(self):
        """Update FPS counter."""
        self.fps_counter += 1
        if time.time() - self.fps_start_time >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.fps_start_time = time.time()
    
    def _draw_ui(self, frame: np.ndarray, faces: List, eyes: List):
        """Draw UI elements on the frame."""
        # Draw face rectangles
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Face', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Draw eye rectangles
        for (x, y, w, h) in eyes:
            color = (0, 0, 255) if self.eyes_closed else (255, 0, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, 'Eye', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Draw status information
        status_text = f"Blink Count: {self.blink_count}"
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        fps_text = f"FPS: {self.current_fps}"
        cv2.putText(frame, fps_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Draw alert if eyes are closed for too long
        if self.eyes_closed and time.time() - self.eyes_closed_start > self.alert_threshold:
            cv2.putText(frame, "ALERT! DROWSINESS DETECTED!", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    
    def _trigger_alert(self):
        """Trigger drowsiness alert."""
        if self.alert_sound:
            try:
                self.alert_sound.play()
            except Exception as e:
                logger.error(f"Failed to play alert sound: {e}")
        
        logger.warning("DROWSINESS ALERT TRIGGERED!")
    
    def run(self):
        """Main detection loop."""
        logger.info("Starting drowsiness detection...")
        logger.info("Press 'q' to quit, 's' to save screenshot")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    logger.error("Failed to read frame from camera")
                    break
                
                # Preprocess frame
                frame = cv2.medianBlur(frame, 5)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces and eyes
                faces, eyes = self._detect_face_and_eyes(frame, gray)
                
                # Analyze eye states
                if faces.size > 0 and len(eyes) >= 2:
                    # Check if both eyes are closed
                    eyes_open = 0
                    for eye in eyes[:2]:  # Check first two eyes
                        if self._analyze_eye_state(frame, gray, faces[0], eye):
                            eyes_open += 1
                    
                    # Update state
                    if eyes_open < 2:  # Both eyes closed
                        if not self.eyes_closed:
                            self.eyes_closed = True
                            self.eyes_closed_start = time.time()
                            self.blink_count += 1
                            logger.info(f"Blink detected! Count: {self.blink_count}")
                    else:
                        self.eyes_closed = False
                    
                    # Check for drowsiness alert
                    if self.eyes_closed and time.time() - self.eyes_closed_start > self.alert_threshold:
                        self._trigger_alert()
                
                # Update FPS
                self._update_fps()
                
                # Draw UI
                self._draw_ui(frame, faces, eyes)
                
                # Display frame
                cv2.imshow('Drowsiness Detection', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"screenshot_{timestamp}.jpg"
                    cv2.imwrite(filename, frame)
                    logger.info(f"Screenshot saved: {filename}")
        
        except KeyboardInterrupt:
            logger.info("Detection stopped by user")
        except Exception as e:
            logger.error(f"Error in detection loop: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up...")
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.quit()
        logger.info("Cleanup complete")


def main():
    """Main entry point."""
    try:
        detector = DrowsinessDetector(camera_index=0, alert_threshold=4.0)
        detector.run()
    except Exception as e:
        logger.error(f"Failed to start drowsiness detector: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
