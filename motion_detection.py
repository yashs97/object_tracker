import numpy as np
import cv2

def check_for_motion(frame,frame1):
	#interesting coordinates
	motion = False
	diff = cv2.absdiff(frame, frame1)
	gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (5,5), 0)
	_, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
	dilated = cv2.dilate(thresh, None, iterations=3)
	contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for contour in contours:
	    (x, y, w, h) = cv2.boundingRect(contour)
	    if cv2.contourArea(contour) > 900:
	        motion = True
	        break
	return motion
