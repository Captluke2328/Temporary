import logging, time, threading
import jetson.inference
import jetson.utils
from camera import *
import arduino as sm

class Track(threading.Thread):

    def __init__(self,C):
        threading.Thread.__init__(self)
        self.daemon = True
        self.ca = C
        self.net = C.net
        self.cam = C.camera
        self.ser = sm.initConnection('/dev/ttyACM0',115200)
     
    # def run(self):
    #     w,h = self.ca.get_image_size()
                
    #     if ((self.info[1]) !=0) and ((self.info[1]) < 500000): 
    #         error = w//2 - self.info[0][0]
    #         self.posX = int(self.pid[0]*error + self.pid[1]*(error-self.pError))
    #         self.posX = int(np.interp(self.posX, [-w//4, w//4], [-35,35]))
    #         self.pError=error
            
    #         sm.sendData(self.ser,[50,self.posX],4)
    #         #print([50,self.posX],4)
        
    #     elif ((self.info[1]) !=0) and ((self.info[1]) > 510000):
    #         sm.sendData(self.ser,[0,0],4)
                
    #     else:
    #         sm.sendData(self.ser,[0,0],4)

    # def trackObject(self,img,det,pid,pError):
    #     self.info = det.Center
    #     self.area = det.Area
    #     self.pid = pid
    #     self.pError = pError

    #     w,h = self.ca.get_image_size()
                
    #     if ((self.area) !=0) and ((self.area) < 500000):
    #         error = w//2 - self.info[0]
    #         self.posX = int(self.pid[0]*error + self.pid[1]*(error-self.pError))
    #         self.posX = int(np.interp(self.posX, [-w//4, w//4], [-35,35]))
    #         self.pError=error
            
    #         sm.sendData(self.ser,[50,self.posX],4)
    #         #print([50,self.posX],4)
        
    #     elif ((self.area) !=0) and ((self.area) > 510000):
    #          sm.sendData(self.ser,[0,0],4)
                
    #     else:
    #         sm.sendData(self.ser,[0,0],4)


    def trackObject(self,img,info,pid,pError):
        self.info = info
        self.pid = pid
        self.pError = pError

        w,h = self.ca.get_image_size()
                
        if ((self.info[1]) !=0) and ((self.info[1]) < 500000):
            error = w//2 - self.info[0][0]
            self.posX = int(self.pid[0]*error + self.pid[1]*(error-self.pError))
            self.posX = int(np.interp(self.posX, [-w//4, w//4], [-35,35]))
            self.pError=error
            
            sm.sendData(self.ser,[50,self.posX],4)
            #print([50,self.posX],4)
        
        elif ((self.info[1]) !=0) and ((self.info[1]) > 510000):
            sm.sendData(self.ser,[0,0],4)
                
        else:
            sm.sendData(self.ser,[0,0],4)

                                    
# class Track:
#     def __init__(self,C):
#         self.ca = C
#         self.net = C.net
#         self.cam = C.camera
#         self.posX = 0
#         self.ser = sm.initConnection('/dev/ttyACM0',115200)
    
#     def trackObject(self,img,info,pid,pError):
#         w,h = self.ca.get_image_size()
                
#         if ((info[1]) !=0) and ((info[1]) < 500000):
#             error = w//2 - info[0][0]
#             posX = int(pid[0]*error + pid[1]*(error-pError))
#             posX = int(np.interp(posX, [-w//4, w//4], [-35,35]))
#             pError=error
            
#             sm.sendData(self.ser,[50,posX],4)
        
#        #elif ((info[1]) !=0) and ((info[1]) > 510000):
#        #     sm.sendData(self.ser,[0,0],4)
            
#         else:
#             sm.sendData(self.ser,[0,0],4)
            
#         return img
            
