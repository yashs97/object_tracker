import numpy as np
import argparse
import cv2 
# from imutils.video import VideoStream
from imutils.video import FPS
import motion_detection as mt
import time


# construct the argument parse 
parser = argparse.ArgumentParser(description='Script to run Object Tracking using opencv')
parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
parser.add_argument("--thr", default=0.6, type=float, help="confidence threshold to filter out weak detections")
parser.add_argument("--frame_count", default='1',help="run the object detector every n frames")
parser.add_argument("--output",default = False,help = "create output video file")
args = parser.parse_args()

# Labels of Network.
labels = { 0: 'background',
    1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
    5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
    10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
    14: 'motorbike', 15: 'person', 16: 'pottedplant',
    17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' }


# Open video file or capture device. 
if args.video:
    cap = cv2.VideoCapture(args.video)
else:
    cap = cv2.VideoCapture(0)

net = cv2.dnn.readNetFromCaffe("mobilenet/MobileNetSSD_deploy.prototxt", "mobilenet/MobileNetSSD_deploy.caffemodel")
tracker = cv2.MultiTracker_create() # create multitracker class
fps = FPS().start()
frame_count = 0
init_once = np.zeros(21)
tracking = np.zeros(21)
detected = 0
if args.output:
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter(args["output"], fourcc, 30,(frame.shape[1], frame.shape[0]), True)
#tracking = False
while True:
    # Capture frame-by-frame
    ret, frame1 = cap.read()
    ret1,frame = cap.read()
    # print("Frame shape: ",frame.shape)
    # print("Frame1 shape: ",frame1.shape)
    # check for motion, if not restart the loop
        # then detect the object
    if mt.check_for_motion(frame,frame1) and frame_count % int(args.frame_count) == 0:
        print('Motion detected')
        frame_resized = cv2.resize(frame,(300,300)) # reshaping frame to (1, 3, 300, 300)
        if tracker and detected == 0:
            blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
            net.setInput(blob)
            detections = net.forward()
            # print("detection shape: ",detections.shape)
            # object to be tracked's probability should be greater than the threshold
            idx = np.argwhere(detections[0, 0, :, 2] >= args.thr)
            for i in range(0,len(idx)):     

                tracking_id = int(detections[0, 0, idx[i], 1]) 
                confidence = detections[0, 0, idx[i], 2]

                #Size of frame resize (300x300)
                cols = frame_resized.shape[1] 
                rows = frame_resized.shape[0]

                # Object location 
                xLeftBottom = int(detections[0, 0, idx[i], 3] * cols) 
                yLeftBottom = int(detections[0, 0, idx[i], 4] * rows)
                xRightTop   = int(detections[0, 0, idx[i], 5] * cols)
                yRightTop   = int(detections[0, 0, idx[i], 6] * rows)
                
                # Factor for scale to original size of frame
                heightFactor = frame.shape[0]/300.0  
                widthFactor = frame.shape[1]/300.0 

                # Scale object detection to frame
                xLeftBottom = int(widthFactor * xLeftBottom) 
                yLeftBottom = int(heightFactor * yLeftBottom)
                xRightTop   = int(widthFactor * xRightTop)
                yRightTop   = int(heightFactor * yRightTop)

                # Draw location of object  
                cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),(0, 0, 255))

                # Draw label and confidence of prediction in frame resized
                label = labels[tracking_id] + ": " + str(confidence)
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                yLeftBottom = max(yLeftBottom, labelSize[1])
                #cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                     # (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                     # (255, 255, 255), cv2.FILLED)
                cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                print(label) # print class and confidence
                rect = ((xLeftBottom), (yLeftBottom), (xRightTop), (yRightTop))

                if init_once[idx[i]] == 0: # initiate tracking class
                    #tracking = True
                    init_once[idx[i]] = 1
                    tracking[idx[i]] = 1 
                    ok = tracker.add(cv2.TrackerKCF_create(),frame,rect)
            (ok, box) = tracker.update(frame)

    frame_count += 1
    fps.update()
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    if args.output:
        writer.write(frame)
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) >= 0:  # Break with ESC 
        break
