import numpy as np
import cv2

def create_boxes(ok,box,frame): #create boxes from trackers
    if ok and len(box) != 0: 
        box = box.squeeze()
        if len(box.shape) == 1: # only one object to be tracked
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 0, 255),3)
        else:
            for i in range(0,box.shape[0]):
                (x, y, w, h) = [int(v) for v in box[i,:]]
                cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 0, 255),3)
