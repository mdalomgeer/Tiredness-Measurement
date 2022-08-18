# Program to detect Driver drowsiness using haar cascade method 
#----------------------------------------------------------------------------------------------

import cv2
import time
from pygame import mixer

# setup for alarm sound -------------------------------------------
mixer.init()
alert=mixer.Sound('beep.wav')


# Capturing video and setting its frame parameter------------------------------
cap = cv2.VideoCapture(0)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH,360)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

# Making face and eye cascade classifier -------------------------------------
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')

# Variables for blink count and clock ---------------------------------
count = 0
clk1 = 0
clk2 = 0

# Infinity loop for video frame analysis and detecting features ------------------------
while True:
    _, img = cap.read()
    img = cv2.medianBlur(img,5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detecting faces using face cascade Classifiers ------------------------------
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Loop for drawing rectangle around faces and detecting eyes ------------
    for x,y,w,h in faces:
        img = cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        # Taking ROI for face---------------------------
        roi_gray = gray[y:y+(h/2), x:x+(w/2)]
        roi_img = img[y:y+(h/2), x:x+(w/2)]

        # Detecting eyes and plotting small rectangles around them ----------
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for ex,ey,ew,eh in eyes:

            # Getting ROI of eye --------------------------------------------
            roi_eye = roi_img[ey:ey+eh, ex:ex+ew]

            # Getting ROI of pupil -----------------------------------------
            roi_pupil = roi_gray[ey+(2*eh/4):ey+(3*eh/4), ex+(ew/4):ex+(3*ew/4)]


            # Thresholding detection -----------------------------------
            threshVal = 50
            blackPixMin = 120
            
            _, roi_pupil = cv2.threshold(roi_pupil,threshVal, 255, cv2.THRESH_BINARY)
            #roi_pupil = cv2.adaptiveThreshold(roi_pupil,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,21,2)
            whitePix = cv2.countNonZero(roi_pupil)
            blackPix = (roi_pupil.size - whitePix)
            
            print 'black = ' + str(blackPix)
            
            
            if blackPix < blackPixMin:
                count = count + 1
                print (str(count) + ". -------------------Blink!--------------------")  
                clk1 = time.clock()
            else:
                clk2 = time.clock()
             
            
# Blink time calculation ----------------------.
    if (clk2 - clk1) <= -4:
        print "ALERT! ALERT! ALERT! ALERT! ALERT! ALERT! ALERT!"
        alert.play()
    
    # Output processed frames ---------------------

    cv2.imshow('Pupil Region', roi_pupil)
    cv2.imshow('eye', roi_eye)

    # While loop escape condition ----------------------
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# end of program ---------------------------------
