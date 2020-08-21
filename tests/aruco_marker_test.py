import cv2
import time
from imutils.video import VideoStream
from droneblocksutils.aruco_utils import detected_markers_image, detect_distance_from_image_center

if __name__ == '__main__':
    vs = VideoStream(src=0).start()
    time.sleep(2)

    while True:
        frame = vs.read()
        image, center_points = detected_markers_image(frame, draw_center=True, draw_reference_corner=True, target_id=5)

        if len(center_points) > 0:
            image, dx, dy, d = detect_distance_from_image_center(image, center_points[0][0], center_points[0][1])
            print(dx, dy, d)

        # Display the resulting frame
        cv2.imshow('ArUco', image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyWindow('ArUco')
