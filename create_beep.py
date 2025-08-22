#!/usr/bin/env python3
"""
Create a simple beep sound file for alerts
==========================================

This script generates a basic beep sound that can be used for drowsiness alerts.
"""

import numpy as np
import wave
import struct

def create_beep_sound(filename="data/sounds/beep.wav", duration=0.5, frequency=800, sample_rate=44100):
    """
    Create a simple beep sound file.
    
    Args:
        filename: Output filename
        duration: Duration in seconds
        frequency: Frequency in Hz
        sample_rate: Sample rate in Hz
    """
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate sine wave
    audio = np.sin(2 * np.pi * frequency * t)
    
    # Normalize and convert to 16-bit integers
    audio = (audio * 32767).astype(np.int16)
    
    # Create WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())
    
    print(f"✅ Created beep sound: {filename}")

if __name__ == "__main__":
    create_beep_sound()
