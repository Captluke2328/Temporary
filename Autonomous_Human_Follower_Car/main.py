import jetson.inference
import jetson.utils
import sys
import threading
import time

import cv2
import collections
import argparse
import sys
import os

from camera import *
from detector import *
from time import sleep
from track import *

os.system ('sudo systemctl restart nvargus-daemon')

pError =0
pid =[0.5,0.4]

if __name__ == "__main__":
    
    print("Setting up the detector")  
    cam = Camera()
    
    while True:           
        try:
            det = detector(cam)
            
            img, fps, info, data = det.get_detections()
            
            cam.frame(img,det.get_state())
                        
            #if det.get_label():
            img = cam.visualise(img,info,data[0],det.get_state())

            frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            
            thread=threading.Thread(target=det.trackImg.trackObject, args=(frame,info,pid,pError))
            thread.start()
               
            cv2.imshow("Capture",frame)
            if cv2.waitKey(1) & 0XFF == ord('q'):
                cam.close_camera()
                break
            
        except Exception as e:
            print(str(e))
    
    cv2.destroyAllWindows()
