import cv2
import imutils
from droneblocksutils.aruco_utils import detect_markers_in_image, detect_distance_from_image_center

if __name__ == '__main__':
    frame = cv2.imread('../test_data/test_porch_2.JPG')
    frame = imutils.resize(frame, width=800)
    image, marker_details = detect_markers_in_image(frame, draw_center=True, draw_reference_corner=True, target_id=None)

    print(frame.shape)
    if len(marker_details) > 0:
        for marker_detail in marker_details:
            center_x, center_y = marker_detail[0]
            print(center_x, center_y)
            image, dx, dy,d = detect_distance_from_image_center(image, center_x, center_y, show_detail=True)
            print(dx,dy,d)

    # Display the resulting frame
    cv2.imshow('ArUco', image)

    cv2.waitKey(0)