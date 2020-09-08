import cv2
import time
from imutils.video import VideoStream
from droneblocksutils.aruco_utils import detect_markers_in_image, detect_distance_from_image_center

if __name__ == '__main__':
    vs = VideoStream(src=0).start()
    time.sleep(2)

    while True:
        frame = vs.read()
        image, marker_details = detect_markers_in_image(frame, draw_center=True, draw_reference_corner=True, target_id=5)

        if len(marker_details) > 0:
            for marker_detail in marker_details:
                center_x, center_y = marker_detail[0]
                image, dx, dy, d = detect_distance_from_image_center(image, center_x, center_y, show_detail=False)
                print(dx, dy, d)

        # Display the resulting frame
        cv2.imshow('ArUco', image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyWindow('ArUco')
