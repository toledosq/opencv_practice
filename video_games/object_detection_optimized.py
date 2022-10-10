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

    def findObjs(self, img, t=0.5, debug=True):
        img_ = img.copy()
        hmap = cv2.matchTemplate(img_, self.o_img, self.method)

        l = list(zip(*(np.where(hmap >= t))[::-1]))
        r = []

        for loc in l:
            tl = loc
            br = (tl[0] + self.ow, tl[1] + self.oh)
            r.append([int(loc[0]), int(loc[1]), self.ow, self.oh])
            
        r, _ = cv2.groupRectangles(r, 1, 0.5)
        
        pts = []
        lenr = len(r)
        if not self.lenr_done:
            print(lenr)
            self.lenr_done = True
        if lenr:
            for (x, y, w, h) in r:
                cx = x + int(w/2)
                cy = y + int(h/2)
                pts.append((cx, cy))

                cv2.drawMarker(img, 
                               (cx, cy), 
                               (255, 0, 255), 
                               markerType=3, 
                               markerSize=40, 
                               thickness=2)
                               
        if debug:
            cv2.imshow('Matches', img)
            
        return pts


if __name__ == '__main__':
    src_img = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
    obj_img = cv2.imread(sys.argv[2], cv2.IMREAD_UNCHANGED)
    thresh = float(sys.argv[3])
    
    OD = ObjectDetect(obj_img)
    OD.findObjs(src_img, thresh)
