import sys

sys.path.append("..")
import cv2
import imutils
from droneblocksutils.aruco_utils import detect_markers_in_image, detect_distance_from_image_center

if __name__ == '__main__':
    frame = cv2.imread('../test_data/test_porch_2.JPG')
    print(f"Before Resize: {frame.shape} (Height (y), Width (x)")
    frame = imutils.resize(frame, width=800)
    original = frame.copy()
    print(f"After Resize: {frame.shape} (Height (y), Width (x)")

    image, marker_details = detect_markers_in_image(frame, draw_center=True, draw_reference_corner=True, target_id=None)

    print(f"Image Center: x,y={frame.shape[1]//2}, {frame.shape[0]//2}")
    print(f"Number of ArUco Markers found: {len(marker_details)}")
    print(f"Marker Details: {marker_details}")
    if len(marker_details) > 0:
        for marker_detail in marker_details:
            marker_center_x, marker_center_y = marker_detail[0]
            print(f"ArUco Marker Center: {marker_center_x}, {marker_center_y}")
            print(f"Id: {marker_detail[1]}")
            image, dx, dy,d = detect_distance_from_image_center(image, marker_center_x, marker_center_y, show_center=True, show_detail=True, show_center_arrow=True)
            print(f"Move Left: {dx} pixels")
            print(f"Move Down: {dy} pixels")
            print(f"Straight Line Distance: {d:.1f}")

    # Display the resulting frame
    cv2.imshow('Original Image', original)
    cv2.imshow('ArUco Marker Test', image)

    cv2.waitKey(0)