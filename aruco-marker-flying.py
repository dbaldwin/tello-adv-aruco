import logging
from droneblocksutils.aruco_utils import detect_markers_in_image, detect_distance_from_image_center
import cv2

# Maximum speed sent to send_rc_control
MAX_SPEED = 40

# if the distance to the target is less than the minimum then just
# set to zero to keep Tello close
MIN_DISTANCE = 30

# Aruco target ID to look for
# None - assumes that there is only a single aruco target in the field of view
# number - then only look for the specified aruco ID
ARUCO_TARGET_ID = None

LOGGER = logging.getLogger()

# Flag to indicate whether the handler method should start to locate aruco markers.
LOCATE_ARUCO_MARKER = False

# Flag indicates if the main handler should send a command to stop
# all motion of the Tello
STOP_TELLO_MOTION = False


def click_capture(event, x, y, flags, param):
    """
    Toggle the LOCATE_ARUCO_MARKER flag for each mouse click

    This will enable/disable the ability to locate Aruco markers.
    """
    global LOCATE_ARUCO_MARKER, STOP_TELLO_MOTION

    if event == cv2.EVENT_LBUTTONDOWN:
        LOGGER.debug(f"click capture: {LOCATE_ARUCO_MARKER}")

        if LOCATE_ARUCO_MARKER == False:
            LOCATE_ARUCO_MARKER = True
        else:
            # we should not locate aruco markers so stop the tello from moving
            STOP_TELLO_MOTION = True

            LOCATE_ARUCO_MARKER = False


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

    :param tello: Reference to the DJITelloPy Tello object.
    :type tello: Tello
    :param frame: image
    :type frame:
    :param fly_flag: True - the fly flag was specified and the Tello will take off. False - the Tello will NOT
                        be instructed to take off
    :type fly_flag:  bool
    :return: None
    :rtype:
    """
    global STOP_TELLO_MOTION, LOCATE_ARUCO_MARKER

    if frame is None:
        return

    (H, W) = frame.shape[:2]

    # if we are actively looking for Aruco markers, put green circle in upper right corner
    # if we are not looking for Aruco markers, put red circle in upper right corner
    if LOCATE_ARUCO_MARKER:
        cv2.circle(frame, center=(frame.shape[1]-10, 10), radius=4, color=(0, 255, 0), thickness=-1)
    else:
        cv2.circle(frame, center=(frame.shape[1] - 10, 10), radius=4, color=(0, 0, 255), thickness=-1)

    # if we are not looking for aruco markers
    if LOCATE_ARUCO_MARKER is False:
        # if the flag to send the stop motion has been set
        if STOP_TELLO_MOTION is True:
            # then send the zero velocity via rc_control to stop
            # any motion of the Tello.
            tello.send_rc_control(0, 0, 0, 0)
            # reset the STOP_TELLO_MOTION flag to false as we have handled the
            # request
            STOP_TELLO_MOTION = False

        return

    # If you get here, we should try to detect Aruco markers in the video frame.
    image, marker_details = detect_markers_in_image(frame, draw_center=True, draw_reference_corner=True,
                                                    target_id=None)

    if len(marker_details) > 0:
        center_x, center_y = marker_details[0][0]
        image, x_distance, y_distance, distance = detect_distance_from_image_center(image, center_x,
                                                                                    center_y)
        LOGGER.debug(x_distance, y_distance, distance)

        if tello and fly_flag:
            l_r_speed = int((MAX_SPEED * x_distance) / (W // 2))
            # *-1 because the documentation says
            # that negative numbers go up but I am
            # seeing negative numbers go down
            u_d_speed = int((MAX_SPEED * y_distance / (H // 2)) * -1)

            print(l_r_speed, u_d_speed, distance)

            # to keep the oscillations to a minimum, if the distance is 'close'
            # then override the speed settings to zero
            try:
                if abs(distance) <= MIN_DISTANCE:
                    u_d_speed = 0
                    l_r_speed = 0
                    LOCATE_ARUCO_MARKER = False
                    print("\tFOUND TARGET")
                    tello.send_rc_control(0, 0, 0, 0)
                    STOP_TELLO_MOTION = False

                else:
                    tello.send_rc_control(l_r_speed, 0, u_d_speed, 0)

            except Exception as exc:
                LOGGER.error(f"send_rc_control exception: {exc}")
