import logging
import cv2
from droneblocksutils.aruco_utils import detect_distance_from_image_center, draw_center_point
import time

LOGGER = logging.getLogger()

# Maximum speed that the Tello will fly
# if the Speed is to high, the Tello will be more
# difficult to control.  As a precaution keep the
# maximum speed reasonable
MAX_SPEED = 25

# maximum number of seconds that the Tello is allowed to fly
# in a direction after selected via a mouse click
# this is a safety precaution so the Tello does not fly
# forever.
MAX_FLYING_TIME = 2  # seconds

# Runtime Parameters
flying_start_time = None
mouse_click_x = -1
mouse_click_y = -1
send_hover_command = True


def click_capture(event, x, y, flags, param):
    """
    Function called by OpenCV to handle mouse events in an image window
    :param event: OpenCV Mouse Event
    :param x: x position in pixels
    :param y: y position in pixels
    :param flags: unused
    :param param: unused
    """
    global mouse_click_x, mouse_click_y, send_hover_command, flying_start_time
    if event == cv2.EVENT_LBUTTONDOWN:
        # if the left mouse button was pressed
        if mouse_click_y == -1 and mouse_click_x == -1:
            # if we have not already collected mouse points
            # then save the new mouse click location
            LOGGER.debug(f"Click Capture: {x},{y}")
            mouse_click_y = y
            mouse_click_x = x
            flying_start_time = time.time()
            send_hover_command = False
        else:
            # we have mouse click points already
            # so clear the mouse click x,y and instruct Tello to hover
            mouse_click_x = -1
            mouse_click_y = -1
            send_hover_command = True


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
    global send_hover_command, flying_start_time, mouse_click_x, mouse_click_y

    if frame is None:
        return
    # get the height and width of the Tello video frame
    (H, W) = frame.shape[:2]

    draw_center_point(frame)

    # if the max flying time has been reached, stop flying
    # safety precaution
    if flying_start_time is not None and time.time() - flying_start_time > MAX_FLYING_TIME:
        mouse_click_x = -1
        mouse_click_y = -1
        send_hover_command = True
        flying_start_time = None

    if mouse_click_x > 0 and mouse_click_y > 0:
        image, x_distance, y_distance, distance = detect_distance_from_image_center(frame, mouse_click_x, mouse_click_y)

        if tello and fly_flag:
            l_r_speed = int((MAX_SPEED * x_distance) / (W // 2))
            # *-1 because the documentation says
            # that negative numbers go up but I am
            # seeing negative numbers go down
            u_d_speed = int((MAX_SPEED * y_distance / (H // 2)) * -1)
            print(l_r_speed, u_d_speed)

            try:
                tello.send_rc_control(l_r_speed, 0, u_d_speed, 0)
            except Exception as exc:
                LOGGER.error(f"send_rc_control exception: {exc}")

    else:
        # no mouse click so just stay put
        if tello and send_hover_command:
            # then have the Tello hover. the send_hover_command
            # will make sure we only do this once.  We dont want to flood
            # the Tello with a lot of commands
            tello.send_rc_control(0, 0, 0, 0)
            send_hover_command = False
