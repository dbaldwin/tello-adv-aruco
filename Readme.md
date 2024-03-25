# Droneblocks Advanced Tello Programming
## Aruco Marker Detections

## Setup
After cloning or downloading the repo

* create a python virtual environment
* `pip install -r requirements.txt`

## Running Tests

### aruco_marker_test

```shell
cd tests
python aruco_marker_test.py
```

This should open two windows.  One of a picture with an aruco marker, and the other of the same picture but the aruco marker identified and a line from the center of the image to the center of the detected aruco marker.

### aruco_mouse_tracking.py

```shell
cd tests
python aruco_mouse_tracking.py
```

This test will show a window with an aruco marker and it will track the mouse position.  There will be a visual indication how far vertically and horizontally the mouse point is from the center of the aruco marker.  It will also show you what the send_rc function call needs to be to more to the center of the aruco marker.

### basic_droneblocks_marker_test.py

```shell
cd tests
python basic_droneblocks_marker_test.py
```

Basic test to detect aruco marker using DroneBlock utilities

### basic_opencv_aruco_marker_test.py

```shell
cd tests
python basic_opencv_aruco_marker_test.py
```

Basic test to detect aruco marker using low level opencv functions

## Examples

### Non-Flying Video Display

This example will connect to the Tello and display the video feed - but it will not start the Tello flying.

```shell
python tello_script_runner.py --handler aruco-marker-flying.py --display-video
```

FAQ:

* Why is the video feed so slow?

We have seen where people have upgraded the DJITelloPy package past the recommended 2.4.0 version.  In later version of DJITelloPy, OpenCV was removed for video capture and replaced with PyAV.  This apparently buffers video differently causing a significant delay.  


## Upgrade Notes ( March 23, 2024 )

* upgrade numpy ( indirectly by upgrading other dependencies )
* upgraded all dependencies in setup.py to the latest or more recent versions 
* aruco_utils.py:8 aruco.Dictionary_get is no longer part of the latest API
* You must pin the DJITelloPy version to 2.4.0 because later versions do not use OpenCV and colors are off because OpenCV uses BGR order and PyAV uses RGB order
* Thread.Event IsSet is deprecated for is_set
