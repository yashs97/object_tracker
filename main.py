import numpy as np
import argparse
import cv2 
import time
from imutils.video import FPS 



# construct the argument parse 
parser = argparse.ArgumentParser(description='Script to run Object trackers using opencv')
parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
parser.add_argument("--thr", default=0.9, type=float, help="confidence threshold to filter out weak detections")
parser.add_argument("--frame_count", default='2',help="run the object detector every n frames")
parser.add_argument("--output",default = False,help = "create output video file")
args = parser.parse_args()

# Labels of Network.
labels = { 0: 'background',
    1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
    5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
    10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
    14: 'motorbike', 15: 'person', 16: 'pottedplant',
    17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' }

lk_params = dict(winSize = (50,50), maxLevel = 4, 
                criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
# Open video file or capture device. 
if args.video:
    cap = cv2.VideoCapture(args.video)
else:
    cap = cv2.VideoCapture(0)

net = cv2.dnn.readNetFromCaffe("mobilenet/MobileNetSSD_deploy.prototxt", "mobilenet/MobileNetSSD_deploy.caffemodel")
fps = FPS().start()
total_frames = 1
_, prev_fram = cap.read()
prev_frame = cv2.cvtColor(prev_fram, cv2.COLOR_BGR2GRAY)
tracker_count = 0
tracking_started = False

if args.output:
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter(args.output, fourcc, 30,(prev_frame.shape[1], prev_frame.shape[0]), True)

while True:
    _,frame = cap.read()
    if frame is None: #end of video file
        print(tracker_count)
        break
    curr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_resized = cv2.resize(frame,(300,300)) # reshaping frame to (1, 3, 300, 300)
    # check for motion, if not restart the loop#then detect the object
    if total_frames % int(args.frame_count)-1 == 0:
        #print('Motion detected')
        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, 
            (frame_resized.shape[1],frame_resized.shape[0]), (127.5, 127.5, 127.5), crop = False)
        net.setInput(blob)
        detections = net.forward()

        centroids = np.zeros([1, 1, 2], dtype=np.float32)
        # object to be tracked's probability should be greater than the threshold
        idx = np.argwhere(detections[0, 0, :, 2] >= args.thr)
        num_detections = len(idx)
        num_centroids = 0
        for i in range(0,len(idx)):     

            tracking_id = int(detections[0, 0, idx[i], 1]) 
            confidence = detections[0, 0, idx[i], 2]

            # Object location 
            xLeftBottom = int(detections[0, 0, idx[i], 3] * frame_resized.shape[1] ) 
            yLeftBottom = int(detections[0, 0, idx[i], 4] * frame_resized.shape[0])
            xRightTop   = int(detections[0, 0, idx[i], 5] * frame_resized.shape[1] )
            yRightTop   = int(detections[0, 0, idx[i], 6] * frame_resized.shape[0])
            
            # Factor for scale to original size of frame
            heightFactor = frame.shape[0]/frame_resized.shape[0]
            widthFactor = frame.shape[1]/frame_resized.shape[1]

            # Scale object detection to frame
            xLeftBottom = int(widthFactor * xLeftBottom) 
            yLeftBottom = int(heightFactor * yLeftBottom)
            xRightTop   = int(widthFactor * xRightTop)
            yRightTop   = int(heightFactor * yRightTop)

            # Draw label and confidence of prediction in frame resized
            label = labels[tracking_id] +": "+ str(confidence)+ ": " + str(total_frames)              
            print(label) # print class and confidence

            x = (xLeftBottom + xRightTop)/2
            y = (yLeftBottom + yRightTop)/2
            centroid = np.array([[[x,y]]],dtype=np.float32)
            if i >= 2 : # 2 or more detections
                dist = np.linalg.norm(centroid.squeeze() - centroids.squeeze(),
                                axis = centroids.squeeze().ndim -1)
                if isinstance(dist,np.float32):
                    min_dist = dist
                else :
                    min_dist = dist[np.argmin(dist)]
                if 20 < min_dist  and num_centroids <= num_detections: # min dist threshold to consider motion
                    frame = cv2.circle(frame, (int(x),int(y)), 15, (0,0,255), -1)
                    #print("Hi")
                    num_centroids += 1
                    tracking_started = True
                    tracker_count += 1
                    centroids = np.append(centroids,centroid,axis = 0)

            else:
                centroids = np.append(centroids,centroid,axis = 0)
                frame = cv2.circle(frame, (int(x),int(y)), 15, (0,0,255), -1)
                num_centroids += 1




    else:
        if len(centroids) and tracking_started and num_detections:
            next1, st, error = cv2.calcOpticalFlowPyrLK(prev_frame, curr_frame,
                                            centroids, None, **lk_params)

            good_new = next1[st==1]
            good_old = centroids[st==1]

            for i, (new, old) in enumerate(zip(good_new, good_old)):
                # Returns a contiguous flattened array as (x, y) coordinates for new point
                a, b = new.ravel()
                c, d = old.ravel()
                distance = np.sqrt((a-c)**2 + (b-d)**2)
                if 20 < distance < 200 and num_centroids <= num_detections: # min dist threshold
                    frame = cv2.circle(frame, (a, b), 15, (0,0,255), -1)
                    num_centroids += 1

            centroids = good_new.reshape(-1, 1, 2)



    total_frames += 1
    fps.update()
    fps.stop()
    # print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    if args.output:
        writer.write(frame)
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) >= 0:  # Break with ESC 
        break
