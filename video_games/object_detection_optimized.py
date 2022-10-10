import sys, os
import cv2
import numpy as np


def findObjs(img, o_img, t=0.5, cmp=cv2.TM_CCOEFF_NORMED, debug=False):
    img_ = img.copy()
    hmap = cv2.matchTemplate(img_, o_img, cmp)

    l = list(zip(*(np.where(hmap >= t))[::-1]))
    r = []

    ow = o_img.shape[1]
    oh = o_img.shape[0]

    for loc in l:
        tl = loc
        br = (tl[0] + ow, tl[1] + oh)
        r.append([int(loc[0]), int(loc[1]), ow, oh])
        
    r, _ = cv2.groupRectangles(r, 1, 0.5)
    
    pts = []
    if len(r):
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
    
    findObjs(src_img, obj_img, thresh)
