import sys, os
import cv2
import numpy as np


class ObjectDetect:

    o_img = None
    ow = 0
    oh = 0
    method = None
    lenr_done = False

    def __init__(self, o_img, method=cv2.TM_CCOEFF_NORMED):
        self.o_img = o_img
        self.ow = self.o_img.shape[1]
        self.oh = self.o_img.shape[0]

        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method


    def find(self, img, t=0.5, maxr=10):
        hmap = cv2.matchTemplate(img, self.o_img, self.method)

        l = list(zip(*(np.where(hmap >= t))[::-1]))
        
        if not l:
            return np.array([], dtype=np.int32).reshape(0, 4)
        
        r = []

        for loc in l:
            r_ = [int(loc[0]), int(loc[1]), self.ow, self.oh]
            r.append(r_)
            r.append(r_)  # Append twice to prevent group miss
            
        r, _ = cv2.groupRectangles(r, 1, 0.5)

        if len(r) > maxr:
            r = r[:maxr]
            
        return r
        
        
    def get_pts(self, r):
        pts = []

        for (x, y, w, h) in r:
            cx = x + int(w/2)
            cy = y + int(h/2)
            pts.append((cx, cy))
            
        return pts
        
        
    def draw_rects(self, img, r):
        mc = (255, 0, 255)        
        for (x, y, w, h) in r:            
            cv2.rectangle(img, 
                           (x, y),
                           (x + w, y + h),
                           mc, 
                           cv2.LINE_4)
        
        return img
        
        
    def draw_cross(self, img, pts):
        mc = (255, 0, 255)
        mt = cv2.MARKER_CROSS
        
        for (cx, cy) in pts:
            cv2.drawMarker(img, (cx, cy), mc, mt)
            
        return img

if __name__ == '__main__':
    src_img = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
    obj_img = cv2.imread(sys.argv[2], cv2.IMREAD_UNCHANGED)
    thresh = float(sys.argv[3])
    
    OD = ObjectDetect(obj_img)
    OD.find(src_img, thresh)
