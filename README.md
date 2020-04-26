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
To run this project, follow these installation steps in order on a Raspberry Pi 4:

```
$ git clone https://github.com/yshah43/object_tracker.git
$ cd object_tracker
$ pip install requirements.txt
$ python main.py
```

## Tracking Algorithm

![alt text](https://github.com/yshah43/object_tracker/blob/master/tracking_algo.png)
