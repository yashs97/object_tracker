# Object Tracker on a Raspberry Pi
Authors: Sterling James and Yash Shah


## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
Object Tracking using a Raspberry Pi 4 and a camera on a Pan Tilt controlled by a Servomotor. An object is detcted using the
Mobilenet SSD object detector and tracked using OpenCV's built in Optical Flow algorithm. The position feedback is sent to the controller for the camera so that it can track the object as long as it is in its line of sight. A red LED on the camera will indicate whether an  object is currently being tracked.

## Technologies
Project is created with:
* Lorem version: 12.3
* Ipsum version: 2.33
* Ament library version: 999
	
## Setup
To run this project, install it locally using npm:

```
$ cd ../lorem
$ npm install
$ npm start
```
