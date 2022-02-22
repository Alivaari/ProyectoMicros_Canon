# Color masking in video for blue

import numpy as np
import cv2 as cv


cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # It converts the BGR color space of image to HSV color space
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
     
    # Threshold of blue in HSV space
    lower_blue = np.array([60, 35, 140])
    upper_blue = np.array([180, 255, 255])
 
    # preparing the mask to overlay
    mask = cv.inRange(hsv, lower_blue, upper_blue)
     
    # The black region in the mask has the value of 0,
    # so when multiplied with original image removes all non-blue regions
    result = cv.bitwise_and(frame, frame, mask = mask)
 
    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('result', result)
    if cv.waitKey(1) == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
