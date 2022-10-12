from csi_camera import CSI_Camera
from detect import *
from camera import *
 
if __name__ == "__main__":
    cam = Camera()
    det = Detect(cam) 
    while True:
        img,info = det.captureimage()
        
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
        cv2.destroyAllWindows()
        
        
    