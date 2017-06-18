#!/usr/bin/env python

from dji_sdk.dji_drone import DJIDrone
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import dji_sdk.msg 
import time
import sys
import math

def display_main_menu():
    print "----------- < Main menu > ----------"
    print "[a] Request to obtain control"
    print "[b] Release control"
    print "[c] Takeoff"
    print "[d] Landing"
    print "[e] Go home"
    print "[f] Gimbal control sample"
    print "[g] Attitude control sample"
    print "[h] Draw circle sample"
    print "[i] Draw square sample"
    print "[j] Take a picture"
    print "[k] Start video"
    print "[l] Stop video"
    print "[m] Local Navi Test"
    print "[n] GPS Navi Test"
    print "[o] Waypoint List Test"
    print "[p] Arm Test"
    print "[q] Disarm Test"
    print "[r] Vrc Test"
    print "[s] Sync Test"
    print "[t] Exit"
    print "[1] "
    print "[2] "
    print "[3] "
    print "[4] "
    print "[5] "
    print "\ninput a/b/c etc..then press enter key"
    print "\nuse `rostopic echo` to query drone status"
    print "----------------------------------------"
    print "input: "

def main():
    print "running"
    drone = DJIDrone()
    
    #$ python object_movement.py --video object_tracking_example.mp4
    if True:
  
        # construct the argument parse and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
            help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=32,
            help="max buffer size")
        args = vars(ap.parse_args())

        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space
        (LR, LG, LB)=(0, 33, 51)
        (HR, HG, HB)=(255, 255, 255)
 
        # initialize the list of tracked points, the frame counter,
        # and the coordinate deltas
        pts = deque(maxlen=args["buffer"])
        counter = 0
        (dX, dY) = (0, 0)
        direction = ""

        # if a video path was not supplied, grab the reference
        # to the webcam
        if not args.get("video", False):
            camera = cv2.VideoCapture(0)

        # otherwise, grab a reference to the video file
        else:
            camera = cv2.VideoCapture(args["video"])
        #############################################################
        objectTracked = False
        x=0
        y=0
        z=0
        angle=0
      

        drone.request_sdk_permission_control()
       
        drone.takeoff()
        print "taking off"
        time.sleep(10)
        print "took off"
        for i in range(60): # 60 times for 3.5 meter 300 for 12.7 meter
            drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, 0, 0, 1, 0)
            time.sleep(0.02)
        print "step 1 done"


        for i in range(300): # 60 times for 3.5 meter 300 for 12.7 meter
            drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, 0, 0, 1, 0)
            time.sleep(0.02)
      
        time.sleep(10)
        print "done"
        
        
        
      
        # keep looping
###################################################################################
        while False:
            start=time.time()
            
            # grab the current frame
            (grabbed, frame) = camera.read()

            Lower = (LR, LG, LB)
            Upper = (HR, HG, HB)
            # if we are viewing a video and we did not grab a frame,
            # then we have reached the end of the video
            if args.get("video") and not grabbed:
                break

            # resize the frame, blur it, and convert it to the HSV
            # color space
            frame = imutils.resize(frame, width=600) #default width=600
            blurred = cv2.GaussianBlur(frame, (11, 11), 0) #(11, 11)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, Lower, Upper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball   number of circle ???
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            delay_time=1

            # only proceed if at least one contour was found
            if len(cnts) > 0: #############################################################################
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum size
                if radius > 5:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2) # draw the circle 
                    cv2.circle(frame, center, 5, (0, 0, 255), -1) #draw the red center
                    #pts.appendleft(center) # This is useless if not have line
                # center is (x,y)
                # print "center"
                # print (center)
                # radius 
                #print radius
            cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (0, 0, 255), 3)
            cv2.putText(frame, "low RGB: {} {} {}, High RGB {} {} {}".format(LR, LG, LB, HR, HG, HB),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)
            
            # show the frame to our screen and increment the frame counter
            cv2.imshow("Frame", frame)
                #center [1]=y center [0]=x x+ to front y+ to right
                # time.sleep(1)
##############################################################################################
            thiscount=0
            if (thiscount>20):
                if len(cnts) > 0:
                    if center[1]>220:
                        if center[0]>350:
                            for i in range(5):
                                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, 1, 1, 0, 0)
                                time.sleep(0.02)   
                                                 
                        elif center[0]<250:
                            for i in range(5):
                                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, -1, 1, 0, 0)
                                time.sleep(0.02)
                             
                        else:
                            for i in range(5):
                                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, 0, 1, 0, 0)
                                time.sleep(0.02)
                             
                    elif center[1]<180:
                        if center[0]>350:
                            for i in range(5):
                                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, 1, -1, 0, 0)
                                time.sleep(0.02)
                             
                        elif center[0]<250:
                            for i in range(5):
                                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, -1, -1, 0, 0)
                                time.sleep(0.02)
                             
                        else:
                            for i in range(5):
                                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, 0, -1, 0, 0)
                                time.sleep(0.02)
                             
                    else:
                        if center[0]>350:
                            for i in range(5):
                                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, 1, 0, 0, 0)
                                time.sleep(0.02)
                             
                        elif center[0]<250:
                            for i in range(5):
                                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, -1, 0, 0, 0)
                                 
                            time.sleep(1)
                        else:
                            for i in range(5):
                                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, 0, 0, -1, 0)
                                 
                            if circle>50:
                                drone.landing()
                                break
                else:
                    for i in range(60):
                        drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, 1, 0, 0, 0)
                         
                thiscount=0
            thiscount+=1        
                        

##############################################################################



            
            key = cv2.waitKey(1) & 0xFF
            # counter += 1
            if key == ord("r"):
                LR+=3
            if key == ord("t"):
                LG+=3
            if key == ord("y"):
                LB+=3
            if key == ord("f"):
                LR-=3
            if key == ord("g"):
                LG-=3
            if key == ord("h"):
                LB-=3
            if key == ord("u"):
                HR+=3
            if key == ord("i"):
                HG+=3
            if key == ord("o"):
                HB+=3
            if key == ord("j"):
                HR-=3
            if key == ord("k"):
                HG-=3
            if key == ord("l"):
                HB-=3
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break
            end=time.time()
            print "end:"
            print (end-start)
        # cleanup the camera and close any open windows
        camera.release()
        cv2.destroyAllWindows()
        drone.release_sdk_permission_control()
        print "opencv ends"
   


    while False:
        display_main_menu()
        main_operate_code = sys.stdin.read(1)
        if main_operate_code == 'a':
            drone.request_sdk_permission_control()
            print "get the control"
        elif main_operate_code == 'b':
            drone.release_sdk_permission_control()
            print "release the control"
        elif main_operate_code == 'c':
            drone.takeoff()
            print "take off"
        elif main_operate_code == 'd':
            drone.landing()
        elif main_operate_code =='e':
            drone.gohome()
        elif main_operate_code == 'f':#gimbal control
            drone.gimbal_angle_control(0, 0, 0, 20)
            time.sleep(2)
            drone.gimbal_angle_control(0, 0, 1800, 20)
            time.sleep(2)
            drone.gimbal_angle_control(0, 0, -1800, 20)
            time.sleep(2)
            drone.gimbal_angle_control(300, 0, 0, 20)
            time.sleep(2)
            drone.gimbal_angle_control(-300, 0, 0, 20)
            time.sleep(2)
            drone.gimbal_angle_control(0, 300, 0, 20)
            time.sleep(2)
            drone.gimbal_angle_control(0, -300, 0, 20)
            time.sleep(2)
            drone.gimbal_speed_control(100, 0, 0)
            time.sleep(2)
            drone.gimbal_speed_control(-100, 0, 0)
            time.sleep(2)
            drone.gimbal_speed_control(0, 0, 200)
            time.sleep(2)
            drone.gimbal_speed_control(0, 0, -200)
            time.sleep(2)
            drone.gimbal_speed_control(0, 200, 0)
            time.sleep(2)
            drone.gimbal_speed_control(0, -200, 0)
            time.sleep(2)
            drone.gimbal_angle_control(0, 0, 0, 20)
        elif main_operate_code == 'g':#attitude control
            drone.takeoff()
            time.sleep(5)

            for i in range(100):
                if i < 90:
                    drone.attitude_control(0x40, 0, 2, 0, 0)
                else:
                    drone.attitude_control(0x40, 0, 0, 0, 0)
                time.sleep(0.02)
            time.sleep(1)

            for i in range(200):
                if i < 180:
                    drone.attitude_control(0x40, 2, 0, 0, 0)
                else:
                    drone.attitude_control(0x40, 0, 0, 0, 0)
                time.sleep(0.02)
            time.sleep(1)


            for i in range(200):
                if i < 180:
                    drone.attitude_control(0x40, -2, 0, 0, 0)
                else:
                    drone.attitude_control(0x40, 0, 0, 0, 0)
                time.sleep(0.02)
            time.sleep(1)

            for i in range(200):
                if i < 180:
                    drone.attitude_control(0x40, 0, 2, 0, 0)
                else:
                    drone.attitude_control(0x40, 0, 0, 0, 0)
                time.sleep(0.02)
            time.sleep(1)

            for i in range(200):
                if i < 180:
                    drone.attitude_control(0x40, 0, -2, 0, 0)
                else:
                    drone.attitude_control(0x40, 0, 0, 0, 0)
                time.sleep(0.02)
            time.sleep(1)

            for i in range(200):
                if i < 180:
                    drone.attitude_control(0x40, 0, 0, 0.5, 0)
                else:
                    drone.attitude_control(0x40, 0, 0, 0, 0)
                time.sleep(0.02)
            time.sleep(1)

            for i in range(200):
                if i < 180:
                    drone.attitude_control(0x40, 0, 0, -0.5, 0)
                else:
                    drone.attitude_control(0x40, 0, 0, 0, 0)
                time.sleep(0.02)
            time.sleep(1)

            for i in range(200):
                if i < 180:
                    drone.attitude_control(0x40, 0, 0, 0, 90)
                else:
                    drone.attitude_control(0x40, 0, 0, 0, 0)
                time.sleep(0.02)
            time.sleep(1)

            for i in range(200):
                if i < 180:
                    drone.attitude_control(0x40, 0, 0, 0, -90)
                else:
                    drone.attitude_control(0x40, 0, 0, 0, 0)
                time.sleep(0.02)
            time.sleep(1)

            drone.landing()

        elif main_operate_code == 'h':#draw circle
            R = 2
            V = 2
            # start to draw circle 
            for i in range(300):
                vx = V * math.sin((V/R)*i/50.0)
                vy = V * math.cos((V/R)*i/50.0)
    
                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, vx, vy, 0, 0)
                time.sleep(0.02)
        elif main_operate_code == 'i':#draw square
            # draw square sample
            for i in range(60):
                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, 3, 3, 0, 0)
                time.sleep(0.02)
            for i in range(60):
                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, -3, 3, 0, 0)
                time.sleep(0.02)
            for i in range(60):
                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, -3, -3, 0, 0)
                time.sleep(0.02)
            for i in range(60):
                drone.attitude_control(DJIDrone.HORIZ_POS|DJIDrone.VERT_VEL|DJIDrone.YAW_ANG|DJIDrone.HORIZ_BODY|DJIDrone.STABLE_ON, 3, -3, 0, 0)
                time.sleep(0.02)
        elif main_operate_code == 'j':#take a picture
            # take a picture
            drone.take_picture()
        elif main_operate_code == 'k':#start video
            # start video
            drone.start_video()
        elif main_operate_code == 'l':#stop video
            # stop video
            drone.stop_video()
        elif main_operate_code == 'm':#local Navi test
            # Local Navi Test 
            drone.local_position_navigation_send_request(-10, -10, 10)
        elif main_operate_code == 'n':#GPS Navi test
            # GPS Navi Test 
            drone.global_position_navigation_send_request(22.535, 113.95, 100)
        elif main_operate_code == 'o':#waypoint List Navi 
            # Waypoint List Navi Test 
            newWaypointList = [
                dji_sdk.msg.Waypoint(latitude = 22.535, longitude = 113.95, altitude = 100, staytime = 5, heading = 0),
                dji_sdk.msg.Waypoint(latitude = 22.535, longitude = 113.96, altitude = 100, staytime = 0, heading = 90),
                dji_sdk.msg.Waypoint(latitude = 22.545, longitude = 113.96, altitude = 100, staytime = 4, heading = -90),
                dji_sdk.msg.Waypoint(latitude = 22.545, longitude = 113.96, altitude = 10, staytime = 2, heading = 180),
                dji_sdk.msg.Waypoint(latitude = 22.525, longitude = 113.93, altitude = 50, staytime = 0, heading = -180)]
            drone.waypoint_navigation_send_request(newWaypointList)
        elif main_operate_code == 'p':#arm test
            drone.arm_drone()
        elif main_operate_code == 'q':#disarm test
            drone.disarm_drone()
        elif main_operate_code == 'r':#vrc test
            drone.vrc_start();
            for i in range(100):
                drone.vrc_control(1024, 1024+660, 1024, 1024)
                time.sleep(0.02)	
            for i in range(100):
                drone.vrc_control(1024, 1024, 1024+660, 1024+660)
                time.sleep(0.02)	
            for i in range(100):
                drone.vrc_control(1024-660, 1024-660)
                time.sleep(0.02)	
            drone.vrc_stop()
        elif main_operate_code == 's':#sync test
            drone.sync_timestamp(50)
        elif main_operate_code == 't':
            return
        else:
            display_main_menu()

if __name__ == "__main__":
    main()
