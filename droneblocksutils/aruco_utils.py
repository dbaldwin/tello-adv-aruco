import cv2
import time
from cv2 import aruco
from imutils.perspective import order_points
import math

# Setup the aruco marker detection
aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
# aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

aruco_params = aruco.DetectorParameters_create()

def draw_center_point(image, center_color=(0,0,255)):
    """
    Given an Image, draw a circle in the center of the image
    :param image: Image to update
    :param center_color: Tuple of (B,G,R) for the color of center circle.  Default - RED
    """
    H, W, _ = image.shape
    # calculate the center of the frame
    centerX = W // 2
    centerY = H // 2

    # draw a circle in the center of the frame
    cv2.circle(image, center=(centerX, centerY), radius=5, color=center_color, thickness=-1)


def find_center_point(corners):
    """
    use points that are on the diagonal to calculate the center points
    corners - array of 4 [x,y] arrays.
    corner[0] = [x0,y0]
        corner[0][0] = x0
        corner[0][1] = y0

    """
    center_x = (corners[0][0] + corners[2][0])//2
    center_y = (corners[0][1] + corners[2][1])//2

    return center_x, center_y

def get_aruco_markers(image, target_id=None):

    all_ordered_corners = []
    all_center_points = []
    all_corners = []
    all_ids = []


    # Convert the color frame to grayscale for marker detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

    # corners is an array of all of the markers found
    # corners[n] is a 3 dimensional array of shape:  1,4,2
    # the 1 means there is a single array or corner data
    #   As best I can tell, the first dimension is always 1.  I am not sure under what
    #   circumstances that would be other than 1.
    # the 4,2 indicates
    # the single array has 4 elements, each element is a 2d array of x,y pairs
    # corners[n] = [ [x1,y1], [x2,y2], [x3,y3], [x4,y4] ]
    #     its four corners (top-left, top-right, bottom-right, and bottom-left)
    # where corners[n][0][0] is equal to [x1,y1] and this point is always the reference point no matter
    # where it appears in the orientation of the ArUco code.

    if corners is not None and ids is not None:
        for i, corner in enumerate(corners):
            if target_id is not None and ids[i][0] != target_id:
                continue

            all_corners.append(corner)
            all_ids.append(ids[i][0])
            ordered_corners = order_points(corner[0])
            all_ordered_corners.append(ordered_corners)
            center_pt_x, center_pt_y = find_center_point(ordered_corners)
            all_center_points.append((int(center_pt_x), int(center_pt_y)))


    return all_corners, all_ids, all_ordered_corners, all_center_points


def detect_markers_in_image(image, draw_reference_corner=True, draw_center=True, target_id=None, draw_target_id=True, draw_border=True):
    """

    :param image: image to search for ArUco markers.  Draw bounding boxes.
    :type image:
    :param draw_reference_corner: Every ArUco marker has a reference corner which is the same no
                                    matter the rotation of the marker.
                                    True - find the reference corner and maker it
                                    False - do not mark reference corner
    :type draw_reference_corner: bool
    :param target_id: ArUco ID to detect.  If None, then detect all markers.  if an
                        id, then only the markers with the specified id will be detected
    :type target_id:
    :param draw_target_id: Flag to indicate whether the id should be added to the image.  Default - True
    :type bool:
    :param draw_border: Flag too indicate whether to draw the border around the marker. Defauilt - True
    :type bool:
    :return: image with all found markers highlighted, center dot, ID number added,
                List for each Marker found. The list contains a tuple of the form: ((center_x,center_y),point_id)
    :rtype: image, list
    """
    corners, ids, ordered_corners, center_pts = get_aruco_markers(image, target_id)
    if len(ordered_corners) > 0:
        # ids = ids.flatten()
        for i, id in enumerate(ids):

            if draw_border:
                # Draw a rectangle around the aruco marker no matter the angular distortion
                cv2.line(image, (ordered_corners[i][0][0], ordered_corners[i][0][1]),
                         (ordered_corners[i][1][0], ordered_corners[i][1][1]), (0, 0, 255), 2)
                cv2.line(image, (ordered_corners[i][1][0], ordered_corners[i][1][1]),
                         (ordered_corners[i][2][0], ordered_corners[i][2][1]), (0, 0, 255), 2)
                cv2.line(image, (ordered_corners[i][2][0], ordered_corners[i][2][1]),
                         (ordered_corners[i][3][0], ordered_corners[i][3][1]), (0, 0, 255), 2)
                cv2.line(image, (ordered_corners[i][3][0], ordered_corners[i][3][1]),
                         (ordered_corners[i][0][0], ordered_corners[i][0][1]), (0, 0, 255), 2)

            center_pt_x = center_pts[i][0]
            center_pt_y = center_pts[i][1]

            if draw_center:
                cv2.circle(image, center=(center_pt_x, center_pt_y), radius=4, color=(0, 255, 0), thickness=-1)

            if draw_target_id:
                cv2.putText(image, f"ID: {id}", (int(center_pt_x), int(center_pt_y)), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2, cv2.LINE_AA)  #

            if draw_reference_corner:
                corner_x_y = corners[i][0][0]
                cv2.circle(image, center=(corner_x_y[0], corner_x_y[1]), radius=8, color=(255, 0, 0), thickness=-1)

    if ids is None:
        return image, []
    else:
        # return image, list(zip(center_pts, ids.flatten()))
        return image, list(zip(center_pts, ids))


def detect_distance_from_image_center(image, selected_pt_x, selected_pt_y, show_detail=True, show_center_arrow=True, show_center=True):
    """
    :param image:
    :param selected_pt_x:
    :param selected_pt_y:
    :param show_detail:
    :param show_center:
    :param show_center_arrow:
    """
    H, W, _ = image.shape
    # calculate the center of the frame as this is (ideally) where
    # we will we wish to keep the object
    centerX = W // 2
    centerY = H // 2

    # draw a circle in the center of the frame
    if show_center:
        cv2.circle(image, center=(centerX, centerY), radius=5, color=(0, 0, 255), thickness=-1)

    # Draw line from frameCenter to selected x,y
    if show_center_arrow:
        cv2.arrowedLine(image, (centerX, centerY), (selected_pt_x, selected_pt_y), color=(0, 255, 0), thickness=2)

    x_distance = selected_pt_x - centerX
    y_distance = selected_pt_y - centerY
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    # print(centerX, centerY, mouse_click_x, mouse_click_y, x_distance, y_distance)

    if show_detail:
        # print(pan_error, int(pan_update), tilt_error, int(tilt_update))
        cv2.putText(image, f"dx: {x_distance}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2, cv2.LINE_AA)

        cv2.putText(image, f"dy: {y_distance}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0), 2, cv2.LINE_AA)

        cv2.putText(image, f"D: {distance:.1f}", (20, 110), cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255), 2, cv2.LINE_AA)

    return image, x_distance, y_distance, distance


