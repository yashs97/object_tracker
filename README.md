Object Tracking using a Raspberry Pi 4 and a camera on a Pan-Tilt Hat controlled by a servomotor. 

## Table of Contents
* [Overview](#overview)
* [Parts List](#parts-list)
* [Setup](#setup)
* [Tracking Algorithm](#tracking-algorithm)

## Overview
An object is first detcted using the Mobilenet SSD object detector and tracked using OpenCV's built in Optical Flow algorithm.
The position feedback is sent to the servomotors so that it can track the object as long as it is in the camera's line of sight. 
A red LED indicate whether an  object is currently being tracked.

## Parts List
Project was created with:
* Raspberry Pi 4
* Camera which is compatible with RPI4
* 3D Printed Pan-Tilt Hat
* Servomotors
* Red LED
	
## Setup
Installation steps on a Raspberry Pi 4:

```
$ git clone https://github.com/yshah43/object_tracker.git
$ cd object_tracker
$ pip install requirements.txt
```

To track objects of one category, run
```
$ python single_label_tracking.py
```

To track objects of multiple categories, run
```
$ python multi_label_tracking.py
```

## Tracking Algorithm

Object tracking is a 2 step process where you first detect an object and then track it.
Mobilenet SSD is the backbone architecture for the detector and was implemented using [OpenCV](#https://github.com/opencv/opencv/wiki/Deep-Learning-in-OpenCV)
Optical flow is then used to track the detected object using the [Lucas-Kanade Method](#https://github.com/opencv/opencv/wiki/Deep-Learning-in-OpenCV)

<p align="center">
  <img src="https://github.com/yshah43/object_tracker/blob/master/tracking_algo.png">
</p>
