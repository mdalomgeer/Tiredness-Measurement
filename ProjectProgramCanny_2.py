# Program to detect Driver drowsiness using haar cascade method
#----------------------------------------------------------------------------------------------

import cv2
import time
from pygame import mixer

# setup for alarm sound -------------------------------------------
mixer.init()
alert = mixer.Sound('C:\Users\Alomgir\PycharmProjects\Rington\beep.mp3')


# Capturing video and setting its frame parameter------------------------------
cap = cv2.VideoCapture(1)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH,360)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

# Making face and eye cascade classifier -------------------------------------
face_cascade = cv2.CascadeClassifier('C:\Users\Alomgir\PycharmProjects\haarcascade\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('C:\Users\Alomgir\PycharmProjects\haarcascade\haarcascade_eye.xml')

# Variables for blink count and clock ---------------------------------
count = 0
clk1 = 0
clk2 = 0

# Infinity loop for video frame analysis and detecting features ------------------------
while True:
    _, img = cap.read()
    img = cv2.medianBlur(img,5)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Detecting faces using face cascade Classifiers ------------------------------
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Loop for drawing rectangle around faces and detecting eyes ------------
    for x,y,w,h in faces:
        img = cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        # Taking ROI for face---------------------------
        roi_faceQ = gray[y:y+(h/2), x:x+(w/2)]
        #roi_face = gray[y:y+h, x:x+w]

        # Detecting eyes and plotting small rectangles around them ----------
        eyes = eye_cascade.detectMultiScale(roi_faceQ)
        for ex,ey,ew,eh in eyes:

            # Getting ROI of eye --------------------------------------------
            roi_eye = roi_faceQ[ey:ey+eh, ex:ex+ew]
            #cannyEye = cv2.Canny(roi_eye,100,200)
            # Getting ROI of pupil -----------------------------------------
            roi_pupil = roi_faceQ[ey+(2*eh/4):ey+(3*eh/4), ex+(ew/4):ex+(3*ew/4)]


            # Thresholding using Canny Edge detection -----------------------------------
            whitePixMin = 30

            cannyPupil = cv2.Canny(roi_pupil,100,200)

            whitePix = cv2.countNonZero(cannyPupil)

            print 'white = ' + str(whitePix)

            if whitePix < whitePixMin:
                count = count + 1
                print (str(count) + ". -------------------Blink!--------------------")
                clk1 = time.clock()
            else:
                clk2 = time.clock()


# Blink time calculation ----------------------.
    alertThresh = 4
    if (clk2 - clk1) <= -alertThresh:
        print "ALERT! ALERT! ALERT! ALERT! ALERT! ALERT! ALERT!"
        alert.play()

# Output processed frames ---------------------


    #cv2.imshow('Pupil Region', roi_pupil)
    #cv2.imshow('face', roi_face)
    #cv2.imshow('cannyEye', cannyEye)
    cv2.imshow('eye', roi_eye)
    cv2.imshow('cannyPupil', cannyPupil)


    # While loop escape condition ----------------------
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# end of program ---------------------------------
