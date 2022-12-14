import sys
import cv2
import numpy as np
from time import time
from window_capture_optimized import WC
from object_detection_optimized import ObjectDetect


if len(sys.argv) > 3:
    print(sys.argv)
    thresh = float(sys.argv[3])
else:
    thresh = 0.60

o_img = cv2.imread(sys.argv[2])
o_img = o_img[...,:3]

wincap = WC(sys.argv[1])
OD = ObjectDetect(o_img)
#wincap = WC()
lt = time()

while(True):
    # Get updated image of window
    s = wincap.get_screen()
    
    # Find rects
    r = OD.find(s, thresh)
    o = OD.draw_rects(s, r)
    cv2.imshow('Matches', o)
    
    # debug loop rate
    print(f'FPS {1 / (time() - lt)}', end='\r')
    lt = time()
    
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        print()
        break
    elif cv2.waitKey(1) == ord('s'):
        wincap.screencap()
