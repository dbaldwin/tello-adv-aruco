import cv2
import imutils
from droneblocksutils.aruco_utils import detect_markers_in_image, detect_distance_from_image_center

window_name = "MouseFollow"
original_frame = None

def mouse_move(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        frame = original_frame.copy()

        image, marker_details = detect_markers_in_image(frame, draw_center=True, draw_reference_corner=True,
                                                        target_id=None)

        marker_detail = marker_details[0]
        marker_center_x, marker_center_y = marker_detail[0]
        dx = marker_center_x - x
        dy = marker_center_y - y
        cv2.circle(frame, center=(x, y), radius=8, color=(255, 255, 0), thickness=-1)

        # draw X component
        cv2.arrowedLine(frame, (x, y), (x+dx, y), color=(0, 255, 0), thickness=2)

        # draw Y componoent
        cv2.arrowedLine(frame, (x+dx, y), (marker_center_x, y+dy), color=(255, 0, 0), thickness=2)

        # draw Hypontenuse
        cv2.arrowedLine(frame, (x, y), (marker_center_x, marker_center_y), color=(0, 0, 255), thickness=2)

        cv2.putText(image, f"send_rc_control({dx}, 0, ", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 154, 255), 2, cv2.LINE_AA)

        cv2.putText(image, f"{dx}", (282, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2, cv2.LINE_AA)

        cv2.putText(image, f"{dy*-1}", (440, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 2, cv2.LINE_AA)

        cv2.putText(image, f", 0)", (530, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 154, 255), 2, cv2.LINE_AA)



        cv2.imshow(window_name, frame)


if __name__ == '__main__':

    original_frame = cv2.imread('./test_data/test_porch_2.JPG')
    original_frame = imutils.resize(original_frame, width=800)
    frame = original_frame.copy()

    # Display the resulting frame
    cv2.imshow(window_name, frame)

    # register a callback function with OpenCV
    # when there is any mouse activity
    cv2.setMouseCallback(window_name, mouse_move)

    cv2.waitKey(0)