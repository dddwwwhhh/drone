# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
# from pyimagesearch.colorlabeler import ColorLabeler
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
realshape="None"
printshape="None"
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	#help="path to the (optional) video file")
	help="/home/cheng/Desktop/drone/video")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color 
lr,lg,lb=(86,16,17)
hr,hg,hb=(106,236,231)

# lr,lg,lb=(5,50,50)
# hr,hg,hb=(69,255,255)
#light green & blue

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	print("video False")
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	greenLower = (lr, lg, lb) # dark red
	greenUpper = (hr, hg, hb) 
	# grab the current frame
	(grabbed, frame1) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame1, width=600)
	ratio = frame1.shape[0] / float(frame.shape[0])
	v = np.median(frame)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - 0.33) * v))
	upper = int(min(255, (1.0 + 0.33) * v))
	edged = cv2.Canny(frame, lower, upper)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	# cv2.imshow("hsv",hsv)
	mask1 = cv2.inRange(hsv, greenLower, greenUpper)
	edged2 = cv2.Canny(mask1, lower, upper)
	mask2 = cv2.erode(mask1, None, iterations=2)
	
	mask3 = cv2.dilate(mask2, None, iterations=2)
	


	mask4 = cv2.GaussianBlur(mask2, (5, 5), 0)
	
	mask5 = cv2.threshold(mask2, 60, 255, cv2.THRESH_BINARY)[1]


	cv2.imshow("mask1",mask1)
	cv2.imshow("mask2",mask2)
	cv2.imshow("mask2",mask2)
	cv2.imshow("mask3",mask3)
	cv2.imshow("edge",edged)
	cv2.imshow("edge2",edged2)
	# cv2.imshow("4",mask4)
	# cv2.imshow("5",mask5)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	# cv2.imshow("cnts",cnts)
	# cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	# cv2.imshow("cnts1",cnts)
	center = None


	# initialize the shape detector and color labeler
	sd = ShapeDetector()

	# cl = ColorLabeler()
	# only proceed if at least one contour was found
	for c in cnts:
		realshape=sd.detect(c)
		if len(cnts) > 0 and realshape == "square":
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			printshape=realshape
		
			
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			
			if M["m00"]!=0 and radius>10:
				
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

			# only proceed if the radius meets a minimum size
			if radius > 10:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
				pts.appendleft(center)

			

	# loop over the set of tracked points
	for i in np.arange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# check to see if enough points have been accumulated in
		# the buffer
		# if counter >= 10 and i == 1 and pts[-10] is not None:
		# 	# compute the difference between the x and y
		# 	# coordinates and re-initialize the direction
		# 	# text variables
		# 	dX = pts[-10][0] - pts[i][0]
		# 	dY = pts[-10][1] - pts[i][1]
		# 	(dirX, dirY) = ("", "")

		# 	# ensure there is significant movement in the
		# 	# x-direction
		# 	if np.abs(dX) > 20:
		# 		dirX = "East" if np.sign(dX) == 1 else "West"

		# 	# ensure there is significant movement in the
		# 	# y-direction
		# 	if np.abs(dY) > 20:
		# 		dirY = "North" if np.sign(dY) == 1 else "South"

		# 	# handle when both directions are non-empty
		# 	if dirX != "" and dirY != "":
		# 		direction = "{}-{}".format(dirY, dirX)

		# 	# otherwise, only one direction is non-empty
		# 	else:
		# 		direction = dirX if dirX != "" else dirY

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the movement deltas and the direction of movement on
	# the frame
	cv2.putText(frame, printshape, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 3)
	cv2.putText(frame, "dx: {}, dy: {}, lr: {}, lg: {}, lb: {}, hr: {}, hg: {}, hb: {}".format(dX, dY, lr, lg, lb, hr, hg, hb),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 255, 255), 1)

	# show the frame to our screen and increment the frame counter
	cv2.imshow("Frame", frame)
	# cv2.imshow("color",mask)
	key = cv2.waitKey(1) & 0xFF
	counter += 1

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
	elif key == ord("e"):
		lr=lr+2
	elif key == ord("r"):
		lg=lg+2
	elif key == ord("t"):
		lb=lb+2
	elif key == ord("d"):
		lr-=2
	elif key == ord("f"):
		lg-=2
	elif key == ord("g"):
		lb-=2
	elif key == ord("y"):
		hr+=2
	elif key == ord("u"):
		hg+=2
	elif key == ord("i"):
		hb+=2
	elif key == ord("h"):
		hr-=2
	elif key == ord("j"):
		hg-=2
	elif key == ord("k"):
		hb-=2



# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
