import sys
import cv2
import numpy as np

"""
Contour Detection

Join all points along the boundary of an object where pixels have similar color and intensity.

cv2 functions:
- findCountours(image, mode, method)
- drawContours()

cv2 contour modes:
- RETR_TREE -- retrieves all contours & reconstructs hierarchy of nested contours
- RETR_EXTERNAL -- retrives only extreme outer contours
- RETR_LIST -- retrieves all contours w/o any hierarchical relationships
- RETR_CCOMP -- retrieves all contours & constructs 2-level hierarchy (external boundaries + holes)
- RETR_FLOODFILL -- ???

cv2 contour methods:
- CHAIN_APPROX_SIMPLE
- CHAIN_APPROX_NONE

Steps:
1. Convert img to grayscale
2. Apply Binary Thresholding
3. Find the contours
4. Draw the contours on the original image
"""

MODES = {0: 'RETR_TREE',
         1: 'RETR_LIST',
         2: 'RETR_EXTERNAL',
         3: 'RETR_CCOMP',
         4: 'RETR_FLOODFILL'}

# Read image and convert to grayscale
img = cv2.imread(sys.argv[1])
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Binary Thresholding
thresh = 200
max = 255
th, dst = cv2.threshold(img_gray, thresh, max, cv2.THRESH_BINARY)

# Show user threshold results for debugging
cv2.imshow('Binary Image', dst)


for idx, mode in enumerate([cv2.RETR_TREE, cv2.RETR_LIST, cv2.RETR_EXTERNAL, cv2.RETR_CCOMP]):
    # Find the Contours
    contours, hierarchy = cv2.findContours(dst, mode, cv2.CHAIN_APPROX_NONE)

    # Draw contours over original image
    img_copy = img.copy()
    cv2.drawContours(img_copy, 
                     contours=contours,
                     contourIdx=-1,
                     color=(0,255,0),
                     thickness=2,
                     lineType=cv2.LINE_AA)

    # Display results
    cv2.imshow(MODES[idx], img_copy)


"""
Using single channels -- just to see what happens
"""

# COLORS = {0: 'red', 1: 'green', 2: 'blue'}

# Split img into RGB channels
# blue, green, red = cv2.split(img)

# for i, color in enumerate([red, green, blue]):
    # Detect contours using color channel w/o thresholding
    # contours2, hierarchy2 = cv2.findContours(color, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    # Draw Contours on original image
    # img_contour_ = img.copy()
    # cv2.drawContours(img_contour_, 
                     # contours=contours2,
                     # contourIdx=-1,
                     # color=(0,255,0),
                     # thickness=2,
                     # lineType=cv2.LINE_AA)
                     
    # Show results
    # cv2.imshow(f"RGB Contours {COLORS[i]}", img_contour_)
    
cv2.waitKey(0)
cv2.destroyAllWindows