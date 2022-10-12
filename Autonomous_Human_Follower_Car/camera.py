import jetson.inference
import jetson.utils
import cv2
import numpy as np
import sys

class Camera:
    def __init__(self):
        self.net = jetson.inference.detectNet("SSD-Mobilenet-v2", threshold=0.5)
        self.camera = jetson.utils.videoSource("csi://0")
        self.is_active = True
        
    def get_image_size(self):
        self.width = self.camera.GetWidth()
        self.height = self.camera.GetHeight()
        return self.width, self.height

    def close_camera(self):
        self.camera.Close()
    
    def frame(self,img,label):
        
        # Top
        cv2.rectangle(img, (0,0), (self.width,24), (0,0,0), -1)

        # Bottom
        cv2.rectangle(img, (0, self.height-24), (self.width,self.height), (0,0,0), -1)
        
         # Text for State
        state = 'State : {}'.format(label)
        cv2.putText(img, state, (10,self.height-8), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (155,150,255),2)
        
        # Width and Height
        text_dur = 'Width : {} Height: {}'.format(self.width, self.height)
        cv2.putText(img, text_dur, (10,16), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (150,150,255), 2)
        
        return img

    #def visualise(self,img,info,data,label):
    def visualise(self,img,data,label):
        
        info = data.Center
        # Draw Black Rectangle Bottom
        #cv2.rectangle(img, (0,self.height-24),(self.width, self.height),(0,0,0),-1)
        
        # Draw Center Middle Line
        #cv2.line(img,(self.width//2,0),(self.width//2,self.height-24), (255,0,255),3)
        
        # Text for State
        state = 'State : {}'.format(label)
        cv2.putText(img, state, (10,self.height-8), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (155,150,255),2)

        # Draw BBOX around Target
        cv2.rectangle(img,(int(data.Left),int(data.Bottom)), (int(data.Right),int(data.Top)), (247,239,5), thickness=10)

        # Draw Center Image
        cv2.circle(img, (self.width // 2, self.height // 2), 10, (0, 0, 255), cv2.FILLED)
        
        # Draw Center Circle
        cv2.circle(img, (int(info[0]), int(info[1])), 10, (0, 0, 255), thickness=-1, lineType=8, shift=0)
        #cv2.circle(img, (int(info[0][0]), int(info[0][1])), 10, (0, 0, 255), thickness=-1, lineType=8, shift=0)

        # Draw Arrowed Line
        cv2.line(img, (int(self.width // 2), int(self.height // 2)), (int(info[0]), int(info[1])), (255, 0, 0), 5, 10)
        #cv2.line(img, (int(self.width // 2), int(self.height // 2)), (int(info[0][0]), int(info[0][1])), (255, 0, 0), 5, 10)

        return img

        
        
        
