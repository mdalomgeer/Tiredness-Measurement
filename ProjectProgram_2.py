# Program to detect eye blink using haar cascade method by syed sadi, 4th year B.Sc. project.
#----------------------------------------------------------------------------------------------

import cv2
import numpy as np


# Capturing video and setting its frame parameter------------------------------
cap = cv2.VideoCapture(0)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH,360)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

# Making face and eye cascade classifier -------------------------------------
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')

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
            #cv2.rectangle(roi_img, (ex,ey), (ex+ew, ey+eh), (0,0,255), 2)

            # Getting ROI of eye --------------------------------------------
            roi_eye = roi_img[ey:ey+eh, ex:ex+ew]
            #_, roi_eyeth = cv2.threshold(roi_eye,140, 255, cv2.THRESH_BINARY)            
            #roi_eyec = roi_img[ey:ey+eh, ex:ex+ew]

            # Getting ROI for pupil -----------------------------------------
            roi_pupil = roi_gray[ey+(2*eh/4):ey+(3*eh/4), ex+(ew/4):ex+(3*ew/4)]


            # Canny edge detection method -----------------------------------
            #roi_eye = cv2.Canny(roi_eye,100,200)

            '''# Thresholding detection -----------------------------------
            _, roi_pupil = cv2.threshold(roi_pupil,170, 255, cv2.THRESH_BINARY)
            whitePix = cv2.countNonZero(roi_pupil)
            blackPix = (roi_pupil.size - whitePix)
            if blackPix < 30:
                print "Blink!"  '''
            

            '''# Hough Cirlcle detection method ---------------------------
            hcircles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)    
            hcircles = np.uint16(np.around(hcircles))
            for i in hcircles[0,:]:
                # draw the outer circle---
                cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2) '''


            # YCbCr color space detection method ------------------------------
            roi_pupilc = roi_img[ey+(2*eh/4):ey+(3*eh/4), ex+(ew/4):ex+(3*ew/4)]
            roi_pupilc = cv2.cvtColor(roi_pupilc, cv2.COLOR_BGR2YCrCb)
            Skin = 0
            for Y,Cr,Cb in roi_pupil[:]:
                if Y>0 and Y<255:
                    if Cb>77 and Cb<127:
                        if Cr>133 and Cr<173:
                            Skin += 1
            nonSkin = (roi_pupilc.size() - Skin)
            if Skin>nonSkin :
                print 'blink!'
                

            # Template matching method ------------------------------

            # Histogram method --------------------------------------
            
            '''# morphological operators--------------------------------
            kernel = np.ones((1,1),np.uint8)
            roi_pupil = cv2.erode(roi_pupil,kernel,iterations = 1)
            roi_pupil = cv2.dilate(roi_pupil,kernel,iterations = 1) '''
 
   

    # Output processed frames ---------------------

    cv2.imshow('image', roi_pupil)

    # While loop escape condition ----------------------
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# end of program ---------------------------------