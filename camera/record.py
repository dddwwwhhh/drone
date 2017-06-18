import sys

import picamera



with picamera.PiCamera() as camera:

    camera.start_preview()

    camera.start_recording('/home/dronepi2/Desktop/video.h264')
    while (True):
        keyin=sys.stdin.read(0)
        if keyin=='q':
            break

    camera.stop_recording()

    camera.stop_preview()
