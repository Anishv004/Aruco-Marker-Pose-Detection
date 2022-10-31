Aruco Pose Estimation

Pose Estimation of Aruco Markers basically involves 2 steps. First, detecting the maker, and second, estimating the pose of the detected marker.

We detect the Aruco Marker by first converting it to a grayscale image for faster processing, and using the detectMarkers function of aruco module. The detectMarkers function takes the image, the marker disctionary and the detection parameters as arguements and returns 3 data : the ID of the marker, marker corners and a flag variable(returns true or false). 

Once we detect the aruco marker, we have to step in to pose estimation. Now, for Pose estimation, we have to callibarate out camera. Callibaration is usually done by capturing a number of chess board images. 

![image7](https://user-images.githubusercontent.com/100789637/199049228-0c69834a-502c-4774-8e02-4062a1e5b374.png)

From the captured chess board images, we find the corners coordinates and give them as arguements to the calibrateCamera function of aruco module, along with an initialized numpy array of the required dimensions. This function returns a Camera Matrix, distance coefficients, rotational vector and a translational vector. These are the 4 important parameters used for any kind of pose estimation. So, this file(camera_calibaration.py) is going to be something standard, and we can use it in any of our projects. What we do is, we store these parameters in a seperate file in calib_data directory, with an extension of .npz which we can simply access while working on our actual project.

In this project, I haven't captured those set of images manually. Instead, I have used already available images and directly, and followed the rest of the processes as such. The images which I have taken can be referred to from the images directory. 

Coming to the pose estimation, we call these callibaration parameters and store it in different variables first. Whenever an marker gets detected in a frame, we find the number of markers detected in the frame and iterate through each to estimate it's pose. We detect the id of the detected marker as explained above, and display it on the frame using putText function of Aruco library. Now we use the estimatePoseSingleMarkers function, which takes the marker size,corners, camera matrix, distance coefficient as parameters and returns 2 vectors: Rotational and Translational. These are just the transformation of any 3D point expressed in the chessboard coordinate system into the camera coordinate system. This helps us to find the pose accordingly. So, using this, we would now be drawing the pose of the marker in the frame using drawFrameAxes function of Aruco Library. This takes all the 4 parameters of camera callibration data along with the frame, and the length of thickness for drawing the pose. The output can be visualized by imshow function. It would look like the following image. 

<img width="257" alt="id 0" src="https://user-images.githubusercontent.com/100789637/199054913-8b6072f2-2383-4a21-8f5c-684450cdefda.png"> <img width="245" alt="id 1" src="https://user-images.githubusercontent.com/100789637/199054935-6363332a-de27-4669-98aa-b6092ffa9466.png"> <img width="239" alt="id 5" src="https://user-images.githubusercontent.com/100789637/199054943-b15dd65e-7bb4-4827-b51c-fd1765904973.png"> <img width="202" alt="id 15" src="https://user-images.githubusercontent.com/100789637/199054953-87bf78f1-2b5b-4238-9691-695163d15461.png">

The line by line explanation of the code can be understood using the comments in the code.

Note : While running the code for the first time, delete the calib_data directory, run the camera_calibaration.py file first, and run the Aruco_pose_Estimation.py file
