import sys, os
import cv2
import numpy as np


src_img = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
obj_img = cv2.imread(sys.argv[2], cv2.IMREAD_UNCHANGED)

if src_img is None:
    print("Could not read image", src_img)
    exit
elif obj_img is None:
    print("Could not read image", obj_img)
    exit

# Find possible matches for object in screenshot
result = cv2.matchTemplate(src_img, obj_img, cv2.TM_CCOEFF_NORMED)  # using TM_CCOEFF_NORMED as comparison algo

# Get all matching objects
locations = np.where(result >= 0.7)
locations = list(zip(*locations[::-1]))

if locations:
    print("Found matches")
    obj_w = obj_img.shape[1]
    obj_h = obj_img.shape[0]

    for loc in locations:
        top_left = loc
        bottom_right = (top_left[0] + obj_w, top_left[1] + obj_h)
        cv2.rectangle(src_img, 
                      top_left, 
                      bottom_right, 
                      color=(0, 255, 0), 
                      thickness=2, 
                      lineType=cv2.LINE_4)
                              
    cv2.imshow('Matches', src_img)
    cv2.waitKey()
    cv2.imwrite('outputs/matches.jpg', src_img)
