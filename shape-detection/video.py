# USAGE
# python detect_shapes.py --image shapes_and_colors.png

# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments


# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.VideoCapture(0)
mmm=1000
i=0
while True:
	
	(grabbed, frame) = image.read()
	
	
	
		
	if not grabbed:
		break
	resized = imutils.resize(frame, width=600)
	# print frame.shape[0]
	# print resized.shape[0]
	ratio = frame.shape[0] / float(resized.shape[0])
	# print ratio
	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
	cv2.imshow("thresh",thresh)
	# find contours in the thresholded image and initialize the
	# shape detector
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = ShapeDetector()
	# print cnts
	
	# loop over the contours
	for c in cnts:
		# compute the center of the contour, then detect the name of the
		# shape using only the contour
		# print c
		M = cv2.moments(c)
		
		print(M["m00"])
		
		# print (M["m00"])
		# cX = int((M["m10"] / M["m00"]) * ratio)
		# cY = int((M["m01"] / M["m00"]) * ratio)
		shape = sd.detect(c)

		# multiply the contour (x, y)-coordinates by the resize ratio,
		# then draw the contours and the name of the shape on the image
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
		cv2.putText(frame, shape, (300, 300), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (255, 255, 255), 2)

		# show the output image
		cv2.imshow("Image", frame)
		cv2.imshow("blurred", blurred)
		cv2.imshow("thresh", thresh)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

image.release()
cv2.destroyAllWindows()