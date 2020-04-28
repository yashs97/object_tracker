Object Tracking using a Raspberry Pi 4. 

<div class="row">
  <div class="column">
    <video src="pi_view.mp4" style="width:100%">
  </div>
  <div class="column">
    <video src="servo_view.mp4" style="width:100%">
  </div>
</div>

## Table of Contents
* [Overview](#overview)
* [Parts List](#parts-list)
* [Installation and Setup](#setup)
* [Tracking Algorithm](#tracking-algorithm)
* [Hardware Setup](#hardware-setup)

## Overview
An object is first detcted using the Mobilenet SSD object detector and tracked using OpenCV's built in Optical Flow method.
The position feedback is sent to the servomotors so that it can track the object as long as it is in the camera's line of sight. 
A red LED indicate whether an  object is currently being tracked.

## Parts List
Project was created with:
* Raspberry Pi 4
* Camera which is compatible with RPI4
* Adafruit Pan-Tilt Servo Mount
* IR-Cut Pi Camera
* Custom Board
* Red LED
	
## Installation and Setup
Installation steps on a Raspberry Pi 4:

```
$ git clone https://github.com/yshah43/object_tracker.git
$ cd object_tracker
$ pip install requirements.txt
```

To track objects of a single category, run:
```
$ python single_label_tracking.py
```

## Tracking Algorithm

Object tracking is a 2 step process where you first detect an object and then track it.
Mobilenet SSD is the backbone architecture for the detector and was implemented using [OpenCV's Deep Neural Net Module](https://github.com/opencv/opencv/wiki/Deep-Learning-in-OpenCV). Optical flow then tracks the detected object using the [Lucas-Kanade Method](https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html).


Real time performance on a Rasperry Pi without a hardware accelerator was achieved by:
* Detecting new objects every 10th frame 
* Tracking the detected object using Optical Flow
* Detecting and tracking only one category (person by default, check the .py files for other options.

All the code can be found in [single_label_tracking.py file](single_label_tracking.py)

Note: [Multi-label tracking algorithm](multi_label_tracking.py) can track objects of 20 different categories but the hardware implementation for it is outside the scope of this project.


<p align="center">
<img  height = "500" src="tracking_algo.png">
</p>


## Hardware Setup

The hardware for this project consists of a RPI 4, an adafruit pan-tilt servo mount, a ir-cut pi camera, and a custom board. The board is similar to some of the adafruit pi hats in that it uses a PCA9685 (a) i2c led driver to send pwm signals. There are dedicated connections on the top of the board to drive the servos (c), but they do not work for some reason and we do not have any test equipment (due to COVID19), so the servos are driven by a  TB6612 h-bridge driver (b) connected to the pwm controller. This was intended for driving dc motors and is functionally identical to the adafruit DC motor hat, but the servos are controllable through it so as long as it works right? Custom code was written to drive the servos in servo_control.py
For the control system, an error signal in both x and y directions are computed from the centroid found by the object tracker compared with the center of the image. This signal is modulated by a proportional gain of kx = 0.01 and ky = 0.01. The starting positions of x = 0d and y = -30d were also determined experimentally

These values were found experimentally. The response time is slightly on the slower side, and this could be improved by adding an integrator to the control system. Due to time constraints and the slightly varying update time of the object tracker, this was not pursued. This could be a future work section.

The schematic on the left below shows all circuitry associated with driving the servos and the one on the right is our custom board.

<div class="row">
  <div class="column">
    <img src="servo_circuit.png" style="width:100%">
  </div>
  <div class="column">
    <img src="custom board.png" style="width:100%">
  </div>
</div>

