#!/usr/bin/env python

from dji_sdk.dji_drone import DJIDrone
from pyimagesearch.shapedetector import ShapeDetector

from collections import deque
import numpy as np
import argparse
import imutils
import cv2

import dji_sdk.msg 
import time
import sys
import math


drone = DJIDrone()


def main():
    start_x, start_y, start_z=getinfor() # starting position
    stage=1 # set stage
    realshape="None"
    printshape="None"
    
    counter = 0 #counter is for performance 
    c2, c3, c4, c5,c6,c7,c8=(True,True,True,True,True,True,True,)
    
    
    


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
    lr,lg,lb=(0,98,98)
    hr,hg,hb=(12,255,255)

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
#####################################################################################################
    # keep looping
    while True:
        target = False
        radius=-1
        isLanded=False
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
        # ratio = frame1.shape[0] / float(frame.shape[0])
        v = np.median(frame)
     
        # apply automatic Canny edge detection using the computed median
        # lower = int(max(0, (1.0 - 0.33) * v))
        # upper = int(min(255, (1.0 + 0.33) * v))
        # edged = cv2.Canny(frame, lower, upper)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        # cv2.imshow("hsv",hsv)
        mask1 = cv2.inRange(hsv, greenLower, greenUpper)
        # edged2 = cv2.Canny(mask1, lower, upper)
        mask2 = cv2.erode(mask1, None, iterations=2)
        
        mask3 = cv2.dilate(mask2, None, iterations=2)
        


        mask4 = cv2.GaussianBlur(mask2, (5, 5), 0)
        
        mask5 = cv2.threshold(mask2, 60, 255, cv2.THRESH_BINARY)[1]


        # cv2.imshow("mask1",mask1)
        # cv2.imshow("mask2",mask2)
        # cv2.imshow("mask2",mask2)
        # cv2.imshow("mask3",mask3)
        # cv2.imshow("edge",edged)
        # cv2.imshow("edge2",edged2)
        # cv2.imshow("4",mask4)
        # cv2.imshow("5",mask5)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        center = None


        # initialize the shape detector and color labeler
        sd = ShapeDetector()

        # cl = ColorLabeler()
        # only proceed if at least one contour was found
        for c in cnts:
            realshape=sd.detect(c)
            if len(cnts) > 0 and realshape == "square" or realshape == "rectangle":
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                printshape=realshape
            
                
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                if radius >10:
                    if M["m00"]!=0 :
                        
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum size
            
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    pts.appendleft(center)
                    target=True
                    # print "center"
                    # print center 
                    # print x 
                    # print y
        # loop over the set of tracked points
        for i in np.arange(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # check to see if enough points have been accumulated in
            # the buffer
            # if counter >= 10 and i == 1 and pts[-10] is not None:
            #   # compute the difference between the x and y
            #   # coordinates and re-initialize the direction
            #   # text variables
            #   dX = pts[-10][0] - pts[i][0]
            #   dY = pts[-10][1] - pts[i][1]
            #   (dirX, dirY) = ("", "")

            #   # ensure there is significant movement in the
            #   # x-direction
            #   if np.abs(dX) > 20:
            #       dirX = "East" if np.sign(dX) == 1 else "West"

            #   # ensure there is significant movement in the
            #   # y-direction
            #   if np.abs(dY) > 20:
            #       dirY = "North" if np.sign(dY) == 1 else "South"

            #   # handle when both directions are non-empty
            #   if dirX != "" and dirY != "":
            #       direction = "{}-{}".format(dirY, dirX)

            #   # otherwise, only one direction is non-empty
            #   else:
            #       direction = dirX if dirX != "" else dirY

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            ## thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            ## cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        # show the movement deltas and the direction of movement on
        # the frame
        cv2.putText(frame, "{} Target{}".format(str(stage), str(target)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (0, 0, 255), 3)
        cv2.putText(frame, "dx: {}, dy: {}, lr: {}, lg: {}, lb: {}, hr: {}, hg: {}, hb: {}, radius: {}".format(dX, dY, lr, lg, lb, hr, hg, hb, radius),
            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.35, (0, 0, 255), 1)

        # show the frame to our screen and increment the frame counter
##        cv2.imshow("Frame", frame)
    ###############################################################
        (lx,ly,lz) = (getinfor())
        if (abs(lx-start_x))>20 or (abs(ly-start_y)>20 or (abs(lz-start_z))>15): #safty area set
            drone.release_sdk_permission_control()
            print "out of range!!"
            break
                
        # Needs counter to slow the remote down speed up the cv2
        counter += 1
        while (counter > 3):
            counter = 0 #reset counter
            
           
            adj_speed=35
            fly_speed=100
            if stage ==1: #take off reach high 
                print "stage1"
                drone.request_sdk_permission_control()
                time.sleep(0.5)
                print "get "
                drone.takeoff()
                print "takeoff"
                time.sleep(5)
                drone.vrc_start();
                time.sleep(0.5)
                for i in range(200):
                    drone.vrc_control(1024, 1024, 1024+150, 1024)
                    time.sleep(0.02)
                #drone.local_position_navigation_send_request(0,0,3)
                print "local"
                stage=2
                drone.vrc_stop()
                print "stage 2"
                
            elif stage ==2:# moving forward and find the object and check distance from 0, savinng local position.
                if c2==True:
                    drone.vrc_start()
                    c2=False
                
                drone.vrc_control(1024, 1024+fly_speed, 1024, 1024)
                print "--------"
                print target    
                print (abs(lx-start_x))
                print (abs(ly-start_y))
                
                if target==True and ((abs(lx-start_x))>3 or (abs(ly-start_y))>3):  
                    drone.vrc_stop()    
                    stage=5
                    x1,y1,z1=lx,ly,lz
                    print "stage 5"
                    
                    

            elif stage ==3:# adjust position on first check point
                if c3==True:
                    drone.vrc_start();
                    c3=False
                if x>400: # right
                    print "right"
                    if y>275: # down
                        print "down"
                        drone.vrc_control(1024+adj_speed, 1024-adj_speed, 1024, 1024)
                    elif y<175: # up
                        print "up"
                        drone.vrc_control(1024+adj_speed, 1024+adj_speed, 1024, 1024)
                    else:
                        drone.vrc_control(1024+adj_speed, 1024, 1024, 1024)

                elif x<200: # left
                    print "left"
                    if y>275:
                        print "down"
                        drone.vrc_control(1024-adj_speed, 1024-adj_speed, 1024, 1024)
                    elif y<175:
                        print "up"
                        drone.vrc_control(1024-adj_speed, 1024+adj_speed, 1024, 1024)
                    else:
                        drone.vrc_control(1024-adj_speed, 1024, 1024, 1024)
                else:
                    if y>275:
                        print "down"
                        drone.vrc_control(1024, 1024+adj_speed, 1024, 1024)
                    elif y<175:
                        print "up"
                        drone.vrc_control(1024, 1024-adj_speed, 1024, 1024)
                    else:
                        drone.vrc_control(1024, 1024, 1024, 1024)
                        stage=4
                        drone.vrc_stop()
                        
                        print x1
                        print y1
                        print "-----"


            elif stage ==4: # auto adjust high
                if c4 ==True:
                    drone.vrc_start();
                    c4=False
                print "stage4"
                #drone.vrc_control(1024+fly_speed, 1024, 1024, 1024)
                if radius == -1:
                    print "radius"
                    print radius
                elif radius<30:
                    
                    print "too high"
                    drone.vrc_control(1024, 1024, 1024-5, 1024)
                elif radius>130:
                    print "too low"
                    drone.vrc_control(1024, 1024, 1024+5, 1024)
                elif radius<130 and radius>30:
                    stage=5
                    drone.vrc_stop()
                    

                
            elif stage ==5:# moving right and check object distance
                if c5==True:
                    drone.vrc_start();
                    c5=False
                print "stage 5"
                drone.vrc_control(1024+fly_speed, 1024, 1024, 1024)
                
                print "--------"
                print target    
                print (abs(lx-x1))
                print (abs(ly-y1))
                
                if target==True and((abs(lx-x1))>4 or (abs(ly-y1))>4) :
                    x2,y2 =lx,ly
                    stage=6
                    drone.vrc_stop()
                    

            elif stage ==6: # second check point adjust
                if c6==True:
                    drone.vrc_start();
                    c6=False
                print  "stage 6"
                if x>400: # right
                    print "right"
                    if y>275: # down
                        print "down"
                        drone.vrc_control(1024+adj_speed, 1024-adj_speed, 1024, 1024)
                    elif y<175: # up
                        print "up"
                        drone.vrc_control(1024+adj_speed, 1024+adj_speed, 1024, 1024)
                    else:
                        drone.vrc_control(1024+adj_speed, 1024, 1024, 1024)

                elif x<200: # left
                    print "left"
                    if y>275:
                        print "down"
                        drone.vrc_control(1024-adj_speed, 1024-adj_speed, 1024, 1024)
                    elif y<175:
                        print "up"
                        drone.vrc_control(1024-adj_speed, 1024+adj_speed, 1024, 1024)
                    else:
                        drone.vrc_control(1024-adj_speed, 1024, 1024, 1024)
                else:
                    if y>275:
                        print "down"
                        drone.vrc_control(1024, 1024+adj_speed, 1024, 1024)
                    elif y<175:
                        print "up"
                        drone.vrc_control(1024, 1024-adj_speed, 1024, 1024)
                    else:
                        drone.vrc_control(1024, 1024, 1024, 1024)
                        stage=4
                        drone.vrc_stop()
                        print "-----"
                        lr,lg,lb=(86,16,17) # change color if needs
                        hr,hg,hb=(106,236,231)
                        stage=7
            elif stage == 7:
                print "stage 7"
                if c7==True:
                    drone.vrc_start();
                    c7=False
                drone.vrc_control(1024, 1024-fly_speed, 1024, 1024)
                
                if target==True and ((abs(lx-x2))>4 or (abs(ly-y2))>4):  
                    stage=8
                    drone.vrc_stop()

            elif stage == 8:
                print "stage 8"
                if c8==True:
                    drone.vrc_start();
                    c8=False
                if x>400: # lower 
                    if y>275: # right 
                        drone.vrc_control(1024+fly_speed, 1024-fly_speed, 1024, 1024)
                    elif y<175: # left
                        drone.vrc_control(1024-fly_speed, 1024-fly_speed, 1024, 1024)
                    else:
                        drone.vrc_control(1024, 1024-fly_speed, 1024, 1024)

                elif x<200: # higher
                    if y>275:
                        drone.vrc_control(1024+fly_speed, 1024+fly_speed, 1024, 1024)
                    elif y<175:
                        drone.vrc_control(1024-fly_speed, 1024+fly_speed, 1024, 1024)
                    else:
                        drone.vrc_control(1024, 1024+fly_speed, 1024, 1024)
                else:
                    if y>275:
                        drone.vrc_control(1024+fly_speed, 1024, 1024, 1024)
                    elif y<175:
                        drone.vrc_control(1024-fly_speed, 1024, 1024, 1024)
                    else:
                        drone.vrc_control(1024, 1024, 1024, 1024)
                        drone.vrc_stop();
                        drone.landing()
                        drone.release_sdk_permission_control()
                        print "Landed"
                        isLanded=True
                        break
                
        if isLanded ==True:
            break

    #################################################################
        if False:
            # cv2.imshow("color",mask)
            key = cv2.waitKey(1) & 0xFF
            # counter += 1

            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                drone.release_sdk_permission_control()
                break
            elif key == ord("e"):
                lr=lr+1
            elif key == ord("r"):
                lg=lg+1
            elif key == ord("t"):
                lb=lb+1
            elif key == ord("d"):
                lr-=1
            elif key == ord("f"):
                lg-=1
            elif key == ord("g"):
                lb-=1
            elif key == ord("y"):
                hr+=1
            elif key == ord("u"):
                hg+=1
            elif key == ord("i"):
                hb+=1
            elif key == ord("h"):
                hr-=1
            elif key == ord("j"):
                hg-=1
            elif key == ord("k"):
                hb-=1

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
##############################################################################
    while False:
        
        main_operate_code = sys.stdin.read(1)
        if main_operate_code == 'a':
            drone.request_sdk_permission_control()
        elif main_operate_code == 'b':
            drone.release_sdk_permission_control()
        elif main_operate_code == 'c':
            drone.takeoff()
        elif main_operate_code == 'd':
            drone.landing()
        elif main_operate_code =='e':
            drone.gohome()
       
        elif main_operate_code == 'g':
            
            A=DJIDrone.HORIZ_POS
            B=DJIDrone.VERT_VEL
            C=DJIDrone.YAW_ANG
            D=DJIDrone.HORIZ_BODY
            E=DJIDrone.STABLE_ON
           
            
            drone.vrc_start();
            for i in range(100):
                drone.vrc_control(1024, 1024+50, 1024, 1024)
                time.sleep(0.02)   
            for i in range(100):
                drone.vrc_control(1024+100, 1024, 1024, 1024)
                time.sleep(0.02) 
            for i in range(100):
                drone.vrc_control(1024, 1024+330, 1024, 1024)
                time.sleep(0.02) 
            for i in range(100):
                drone.vrc_control(1024, 1024-660, 1024, 1024)
                time.sleep(0.02)    
            for i in range(100):
                drone.vrc_control(1024, 1024)
                time.sleep(0.02)    
            drone.vrc_stop()
##            for i in range(200):
##                if i < 90:
##                    drone.velocity_control(A|B|C|D|E, 0, 0, 0, 90)#0x40
##                else:
##                    drone.velocity_control(A|B|C|D|E, 0, 0, 0, 90)
##                time.sleep(0.02)
##            time.sleep(1)

            

        elif main_operate_code == 't':
            return
            

            

           

            #drone.landing()

def getinfor():
    infor = drone.loc()
##    print drone.loc_ref()
##    print infor
    infor =str(infor)
    # print infor
    
    lxi=float(infor[(infor.find ('x:' )+2):infor.find ('\ny:' )])
    
    lyi=float(infor[(infor.find ('y:' )+2):infor.find('\nz:')])
    
    
    lzi=float(infor[(infor.find ('z:' )+2):])
    

  

    return lxi, lyi , lzi



        
if __name__ == "__main__":
    main()
