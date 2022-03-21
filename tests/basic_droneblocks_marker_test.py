import sys

sys.path.append("..")
import cv2
import imutils
from droneblocksutils.aruco_utils import detect_markers_in_image

if __name__ == '__main__':

    # Read in an image
    # resize so it is easier to view
    # convert to gray scale, because ArUco package requires a gray scale image
    # image = cv2.imread('../test_data/two_aruco_markers.JPG')
    image = cv2.imread('../test_data/test_porch_2.JPG')

    image = imutils.resize(image, width=800)
    image, marker_details = detect_markers_in_image(image, draw_center=True,
                                                    draw_reference_corner=True,
                                                    target_id=None,
                                                    draw_target_id=True,
                                                    draw_border=True)

    # marker_details:
    #   list of each marker found
    #       each element in list is a list of: (x,y) marker center and marker id
    for marker_detail in marker_details:
        print(marker_detail)

    # Show the image
    cv2.imshow('ArUco.detect_markers', image)

    # Wait until any key is pressed to exit
    cv2.waitKey(0)
