import time
import datetime
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from libcamera import controls
from sense_hat import SenseHat
import cv2

sense=SenseHat()

prev_temperature=sense.get_temperature()
picam2=Picamera2()  ## Create a camera object

dispW=1280
dispH=720
picam2.preview_configuration.main.size= (dispW,dispH)

picam2.preview_configuration.main.format= "RGB888"
picam2.preview_configuration.align() ## aligns the size to the closest standard format
picam2.preview_configuration.controls.FrameRate=30 ## set the number of frames per second, this is set as a request, the actual time it takes for processing each frame and rendering a frame can be different

picam2.configure("preview")

faceCascade=cv2.CascadeClassifier("../../Python/haarcascade_frontalface_default.xml")
count_faces = 0

# faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
while True:
    pressure=sense.get_pressure()
    temperature=sense.get_temperature()
    temperature=round(temperature,1) ## round temperature to 1 decimal place
    humidity=sense.get_humidity()
    
    # if there are no contours
    if (temperature - prev_temperature >= 1 or prev_temperature - temperature >=1):
        picam2.start()
        
        frame=picam2.capture_array() ## frame is a large 2D array of rows and cols and at intersection of each point there is an array of three numbers for RGB i.e. [R,G,B] where RGB value ranges from 0 to 255
        frameGray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(frameGray,1.3,5)
        
        print(faces)
        count_faces += len(faces)
        
        for face in faces:
            x,y,w,h=face
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
        cv2.imshow("Camera Frame", frame)
        time.sleep(0.5)
        key=cv2.waitKey(1) & 0xFF
        
        # cv2.imshow("piCamera2", frame) ## show the frame
        # key=cv2.waitKey(1) & 0xFF
        
        if key ==ord(" "):
            cv2.imwrite("frame-" + str(time.strftime("%H:%M:%S", time.localtime())) + ".jpg", frame)
        if key == ord("q"): ## stops for 1 ms to check if key Q is pressed
            break

        print("Total faces detected: " + str(count_faces))                                  
        
cv2.destroyAllWindows()
