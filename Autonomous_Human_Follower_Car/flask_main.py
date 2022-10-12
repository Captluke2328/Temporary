from flask import Flask, Response, render_template
import cv2
import jetson.inference
import jetson.utils
import sys
#import threading
import time

import sys
import os

from camera import *
from detector import *
from time import sleep
from track import *
import arduino as sm

os.system ('sudo systemctl restart nvargus-daemon')

pError =0
pid =[0.5,0.4]

# Frame sent to Flask object
global video_frame
video_frame = None

# Use locks for thread-safe viewing of frames in multiple browsers
global thread_lock
thread_lock = threading.Lock()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def main():
    global video_frame,thread_lock
    print("Setting up the detector")  
    
    cam = Camera()

    while True:
        det = detector(cam)
        
        img, fps,info, data = det.get_detections()

        cam.frame(img,det.get_state())

        # if data[0].ClassID == 1:
        #     img = cam.visualise(img,data[0],det.get_state())
        #     det.track.trackObject(img,info,pid,pError)
        #     # det.track.trackObject(img,data[0],pid,pError)
        # else:
        #     det.track.trackObject(img,[[0,0],0],pid,pError)
            #sm.sendData(det.track.ser,[0,0],4)
            
        if det.get_label():
            img = cam.visualise(img,data[0],det.get_state())
            #img = cam.visualise(img,info,data[0],det.get_state())

        #det.track.trackObject(img,data[0],pid,pError)
        det.track.trackObject(img,info,pid,pError)
             
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        
        with thread_lock:
            video_frame = frame.copy() 
        
def encode_cam():
    global thread_lock
    while True:
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
                    
            success, encoded_image = cv2.imencode('.jpg', video_frame)
            frame = encoded_image.tobytes()
            if not success:
                continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(encode_cam(),mimetype = 'multipart/x-mixed-replace; boundary=frame')  

if __name__ == '__main__':
    init= threading.Thread(target=main)
    init.daemon = True
    init.start()
    app.run(host='192.168.8.121',port=80, threaded=True)
    
    


