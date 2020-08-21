import logging
from droneblocksutils.aruco_utils import detected_markers_image, detect_distance_from_image_center

MAX_SPEED = 25

# Aruco target ID to look for
# None - assumes that there is only a single aruco target in the field of view
# number - then only look for the specified aruco ID
ARUCO_TARGET_ID = None

LOGGER = logging.getLogger()

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
    pass


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
    if frame is None:
        return

    image, center_points = detected_markers_image(frame, draw_center=True, draw_reference_corner=True, target_id=None)

    if len(center_points) > 0:
        image, x_distance, y_distance, distance = detect_distance_from_image_center(image, center_points[0][0], center_points[0][1])
        print(x_distance, y_distance, distance)

        if tello and fly_flag:
            # left/right: -100/100
            l_r_speed = x_distance
            if l_r_speed < 0:
                l_r_speed = max(-MAX_SPEED, l_r_speed)
            else:
                l_r_speed = min(MAX_SPEED, l_r_speed)

            u_d_speed = y_distance * -1 # *-1 because the documentation says
                                        # that negative numbers go up but I am
                                        # seeing negative numbers go down
            if u_d_speed < 0:
                u_d_speed = max(-MAX_SPEED, u_d_speed)
            else:
                u_d_speed = min(MAX_SPEED, u_d_speed)

            try:
                tello.send_rc_control( l_r_speed, 0, u_d_speed, 0)
            except Exception as exc:
                LOGGER.error(f"send_rc_control exception: {exc}")

    else:
        # no mouse click so just stay put
        if tello:
            tello.send_rc_control(0, 0, 0, 0)