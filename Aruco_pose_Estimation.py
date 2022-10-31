import cv2 as cv
from cv2 import aruco
import numpy as np

calib_data_path = "calib_data/MultiMatrix.npz"
# Referring to the data stored after running camera_callibaration file

calib_data = np.load(calib_data_path)
print(calib_data.files)

# Four parameters will get returned by the callibaration file. Calling those for pose estimation 
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]

MARKER_SIZE = 8  # centimeters

marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

param_markers = aruco.DetectorParameters_create()

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Converting the videocapture into grayscale and undergoing the subsequent steps
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detecting the markers
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )
    
    if marker_corners:      # Set of statements if marker is detected
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            marker_corners, MARKER_SIZE, cam_mat, dist_coef
        )  
        # This function returns to lists rVec and tVec which are ntg but the roational and translational vectors.
        
        # The marker coordinate system is centered on the middle (by default) or on the top-left corner of the 
        # marker, with the Z axis perpendicular to the marker plane. estimateParameters defines the coordinates 
        # of the four corners of the marker in its own coordinate system (by default) are: 
        # (-markerLength/2, markerLength/2, 0), (markerLength/2, markerLength/2, 0), (markerLength/2, -markerLength/2, 0), 
        # (-markerLength/2, -markerLength/2, 0)

        total_markers = range(0, marker_IDs.size) # Detects the number of markers detected at any particular instance
        
        # Iterating through each of the detected markers using a for loop
        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            # Drawing a sketch over the detected marker first
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            # Reshaping the corners to 2D form
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)

            # Storing the 4 corners of the detected markers in seperate variables to call them later 
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()

            # Drawing the pose (axis) over the marker
            point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
            # Syntax - drawFrameAxes(camera_frame, camera_matrix(from callibaration data), dist_coeff(from callibaration data), length,thickness)
            
            # Displaying the IDs over the detected Aruco Marker
            cv.putText(
                frame,
                f"id: {ids[0]}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )

    # Displaying the frame
    cv.imshow("frame", frame)

    key = cv.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv.destroyAllWindows()