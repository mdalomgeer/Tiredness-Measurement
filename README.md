# Tiredness measurement using computer vision

Code from our study on detecting tiredness from eye closure with a webcam:

> Hussein MA, Noman MTB, Ahad MAR. A Study on Tiredness Measurement using Computer Vision. Journal of the Institute of Industrial Applications Engineers. 2019;7(4):110-117. https://doi.org/10.12792/JIIAE.7.110

The PDF of the paper is in this repository.

## How it works

1. Find the face and the eyes in each frame with Haar cascades (OpenCV).
2. Decide whether the eyes are open or closed. We tried two ways: counting dark pixels after thresholding, and Canny edge detection on the eye region.
3. If the eyes stay closed longer than a set time, play a beep and show a warning.

## Files

- `ProjectProgram_2.py`, `ProjectProgramThresh_2.py`, `ProjectProgramCanny_2.py`, `ProjectProgramModified_2.py`: the original scripts used in the study
- `src/`: a later, tidier version of the same detector (`drowsiness_detector.py`, with settings in `config.py`)
- `models/`: the Haar cascade files
- `Image Data.rar`: sample images
- `demo.py`, `quick_start.py`: small scripts to try it out

## Running it

You need Python 3 and a webcam.

```
pip install -r requirements.txt
python src/drowsiness_detector.py
```

Press `q` to quit and `s` to save a screenshot. Thresholds and the alert time are in `src/config.py`. Detection depends a lot on lighting, so expect to adjust them.

## Contact

Md Alomgeer Hussein, mdalomh1@umbc.edu
