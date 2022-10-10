import sys
import cv2
import numpy as np

"""
Blob Detection

1. Thresholding: Convert the image into multiple binary images by thresholding source img
    w/ thresholds starting at minThreshold and continuing until maxThreshold at thresholdStep

2. Grouping: In each binary image, connected white pixels are grouped together

3. Merging: The centers of the groups are computed, and groups closer than minDistBetweenBlobs are merged

4. Center & Radius: The centers and radii of the new merged blobs are computed and returned

"""

"""
Available filters:
- Color
- Size
- Shape
- Circularity
- Convexity
- Inertia Ratio
"""
input_path = sys.argv[1]
im = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

if im is None:
    print("Could not read", input_path)
    exit

# Set up SimpleBlobDetector_Params object
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10
params.maxThreshold = 200

# Filter by Area
params.filterByArea = True
params.minArea = 1500

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

# Create a detector with the params
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs
keypoints = detector.detect(im)

# Draw detected blobs as red circles
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS matches circles to the size of blobs
im_w_keypoints = cv2.drawKeypoints(im, 
                                   keypoints, 
                                   np.array([]), 
                                   (0,0,255), 
                                   cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("Keypoints", im_w_keypoints)
cv2.waitKey(0)
