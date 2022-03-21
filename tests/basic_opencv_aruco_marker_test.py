import sys

sys.path.append("..")

import cv2
from cv2 import aruco
import imutils

"""
This script will use OpenCV to detect ArUco markers in an image, and draw a 
red bounding box around the detected marker
"""

if __name__ == '__main__':

    aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

    aruco_params = aruco.DetectorParameters_create()

    # Read in an image
    # resize so it is easier to view
    # convert to gray scale, because ArUco package requires a gray scale image
    image = cv2.imread('../test_data/test_porch_2.JPG')
    image = imutils.resize(image, width=800)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # call the detectMarkers function from the OpenCV ArUco package
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

    for id in ids:
        print(id)

    print(corners)
    for corner in corners:
        print(corner)
    """
    output:
    ID: [5]  array of ids
    
    Corner: array of an array of corners where each corner is an  array of x,y values
    
    [[[112. 418.]
      [215. 417.]
      [213. 511.]
      [112. 512.]]]
    """

    # Retrieve the actual values to use later
    # notice the awkward mutliple indexing to get values
    ID = ids[0][0]
    Corner1 = corners[0][0][0]
    Corner2 = corners[0][0][1]
    Corner3 = corners[0][0][2]
    Corner4 = corners[0][0][3]

    print("------ ArUco Marker Details -------")
    print(ID)
    print(Corner1)
    print(Corner2)
    print(Corner3)
    print(Corner4)

    # Draw a box around the ArUco marker from corner to corner
    # on all 4 sides
    cv2.line(image, (int(Corner1[0]), int(Corner1[1])),
             (int(Corner2[0]), int(Corner2[1])), (0, 0, 255), 2)

    cv2.line(image, (int(Corner2[0]), int(Corner2[1])),
             (int(Corner3[0]), int(Corner3[1])), (0, 0, 255), 2)

    cv2.line(image, (int(Corner3[0]), int(Corner3[1])),
             (int(Corner4[0]), int(Corner4[1])), (0, 0, 255), 2)

    cv2.line(image, (int(Corner4[0]), int(Corner4[1])),
             (int(Corner1[0]), int(Corner1[1])), (0, 0, 255), 2)

    # Show the image
    cv2.imshow('ArUco.detect_markers', image)

    # Wait until any key is pressed to exit
    cv2.waitKey(0)
