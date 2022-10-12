import jetson.inference
import jetson.utils
import cv2
import numpy as np
from camera import *
from track import *

class detector:
    def __init__(self,C):
        self.ca = C
        self.net = C.net
        self.cam = C.camera
        self.label = False
        self.state = "Searching"
        #self.trackImg = Track(C) 
 
        self.track = Track(C)
        self.track.start()
        
    def get_label(self) ->str:
        return self.label
    
    def get_state(self) ->str:
        return self.state
        
    def get_detections(self):
        while True:
            w,h = self.ca.get_image_size()
            
            myobjectListC = []
            myobjectListArea = []
            data = []
            img = self.cam.Capture()
            detections = self.net.Detect(img, overlay="box")
            
            ID = None
            
            for detection in detections: 
                #if detection.ClassID == 1:   
                ID       = detection.ClassID
                top      = int(detection.Top)
                left     = int(detection.Left)
                bottom   = int(detection.Bottom)
                right    = int(detection.Right)
                area     = int(detection.Area)
                location = detection.Center
                item     = self.net.GetClassDesc(ID)
                
                cx       = location[0]
                cy       = location[1]
                
                myobjectListArea.append(area)
                myobjectListC.append([cx,cy])
                data.append(detection)

            fps = self.net.GetNetworkFPS()

            if len(myobjectListArea) > 0:
                if ID == 1:
                    self.label = True
                    self.state = "Tracking"
                    i = myobjectListArea.index(max(myobjectListArea))
                    return jetson.utils.cudaToNumpy(img),fps, [myobjectListC[i],myobjectListArea[i]], data 

                else: 
                    self.label = False
                    self.state = "Searching"

                    return jetson.utils.cudaToNumpy(img),fps, [[0,0],0], data

        '''
        
        for detection in detections:
            try:
                ID       = detection.ClassID
                top      = int(detection.Top)
                left     = int(detection.Left)
                bottom   = int(detection.Bottom)
                right    = int(detection.Right)
                area     = int(detection.Area)
                location = detection.Center
                item     = self.net.GetClassDesc(ID)
                
                cx       = location[0]
                cy       = location[1]
                
                myobjectListArea.append(area)
                myobjectListC.append([cx,cy])
                    
            except:
                pass
        
        fps = self.net.GetNetworkFPS()
        
        if ID==1:
            #self.label = True
            #self.state = "Tracking"
            i = myobjectListArea.index(max(myobjectListArea))
            return jetson.utils.cudaToNumpy(img),fps, [myobjectListC[i],myobjectListArea[i]]

        else:
            # self.label = False
            #self.state = "Searching"
            return jetson.utils.cudaToNumpy(img),fps, [[0,0],0]
                         
        '''
        
