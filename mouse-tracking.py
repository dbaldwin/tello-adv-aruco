import cv2
import imutils

window_name = "MouseFollow"
original_frame = None


def mouse_movement_detected(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        frame = original_frame.copy()
        (H, W) = frame.shape[:2]
        center_x = W // 2
        center_y = H // 2

        # find the difference between the center of the image
        # and the mouse pointer (x,y)
        dx = center_x - x
        dy = center_y - y

        # draw a circle at the center of the image
        cv2.circle(frame, center=(x, y), radius=8, color=(255, 255, 0), thickness=-1)

        # draw X component
        cv2.arrowedLine(frame, (x + dx, y), (x, y), color=(0, 255, 0), thickness=2)

        # draw Y component
        cv2.arrowedLine(frame, (center_x, y + dy), (x + dx, y), color=(255, 0, 0), thickness=2)

        # draw Hypotenuse
        cv2.arrowedLine(frame, (center_x, center_y), (x, y), color=(0, 0, 255), thickness=2)

        # instead of using actual pixel locations, I would like to
        # show grid coordinates
        grid_x = round((dx * 9) / 383, 1) * -1
        grid_y = round((dy * 9) / 383, 1) * -1

        # show in the image what the send_rc_control command would look like
        cv2.putText(frame, f"send_rc_control(", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 154, 255), 2, cv2.LINE_AA)

        cv2.putText(frame, f"{grid_x}, ", (280, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2, cv2.LINE_AA)

        cv2.putText(frame, f" 0,", (360, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 154, 255), 2, cv2.LINE_AA)

        cv2.putText(frame, f"{grid_y}", (440, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 2, cv2.LINE_AA)

        cv2.putText(frame, f", 0)", (530, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 154, 255), 2, cv2.LINE_AA)

        # show the updated image in the OpenCV window
        cv2.imshow(window_name, frame)


if __name__ == '__main__':
    original_frame = cv2.imread('test_data/grid_image.jpg')
    print(f"Shape: {original_frame.shape}")
    original_frame = imutils.resize(original_frame, width=800)
    frame = original_frame.copy()

    # Display the resulting frame
    cv2.imshow(window_name, frame)

    # register a callback function with OpenCV
    # when there is any mouse activity
    cv2.setMouseCallback(window_name, mouse_movement_detected)

    # wait for any key to be pressed too exit
    cv2.waitKey(0)
