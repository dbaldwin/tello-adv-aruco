import logging
import cv2
from droneblocksutils.aruco_utils import detect_distance_from_image_center, draw_center_point

MAX_SPEED = 25

LOGGER = logging.getLogger()

mouse_click_x = -1
mouse_click_y = -1
CLEAR_MOUSE_POINTS = False

def click_capture(event, x, y, flags, param):
    global mouse_click_x, mouse_click_y, CLEAR_MOUSE_POINTS
    if event == cv2.EVENT_LBUTTONDOWN:
        if mouse_click_y == -1 and mouse_click_x == -1:
            LOGGER.debug(f"Click Capture: {x},{y}")
            mouse_click_y = y
            mouse_click_x = x
        else:
            # we have mouse click points so clear them
            mouse_click_x = -1
            mouse_click_y = -1
            CLEAR_MOUSE_POINTS = True


def init(tello, fly_flag=False):
    """

    :param tello: Reference to the DJITelloPy Tello object.
    :type tello: Tello
    :param fly_flag: True - the fly flag was specified and the Tello will take off. False - the Tello will NOT
                        be instructed to take off
    :type fly_flag:  bool
    :return: None
    :rtype:
    """
    cv2.setMouseCallback("Tello Video", click_capture)


def handler(tello, frame, fly_flag=False):
    """
        handler method called from tello_script_runner.py

    :param tello: Reference to the DJITelloPy Tello object.
    :type tello: Tello
    :param frame: Tello video frame image
    :type frame: Image
    :param fly_flag: True - the fly flag was specified and the Tello will take off.
                     False - the Tello will NOT be instructed to take off
    :type fly_flag:  bool
    :return: None
    :rtype:
    """
    global CLEAR_MOUSE_POINTS

    if frame is None:
        return

    draw_center_point(frame)

    if mouse_click_x > 0 and mouse_click_y > 0:
        image, x_distance, y_distance, distance = detect_distance_from_image_center(frame, mouse_click_x,
                                                                                    mouse_click_y)
        # print(x_distance, y_distance, distance)

        if tello and fly_flag:
            # left/right: -100/100
            l_r_speed = x_distance
            if l_r_speed < 0:
                l_r_speed = max(-MAX_SPEED, l_r_speed)
            else:
                l_r_speed = min(MAX_SPEED, l_r_speed)

            u_d_speed = y_distance * -1  # *-1 because the documentation says
            # that negative numbers go up but I am
            # seeing negative numbers go down
            if u_d_speed < 0:
                u_d_speed = max(-MAX_SPEED, u_d_speed)
            else:
                u_d_speed = min(MAX_SPEED, u_d_speed)

            try:
                tello.send_rc_control(l_r_speed, 0, u_d_speed, 0)
            except Exception as exc:
                LOGGER.error(f"send_rc_control exception: {exc}")

    else:
        # no mouse click so just stay put
        if tello and CLEAR_MOUSE_POINTS:
            # then have the Tello hover
            tello.send_rc_control(0, 0, 0, 0)
            CLEAR_MOUSE_POINTS = False
