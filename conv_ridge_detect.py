import sys, os
import cv2
import numpy as np

image_path = sys.argv[1]
print(image_path)

img = cv2.imread(image_path)
if img is None:
    print("Could not read", image_path)
    
kernel = np.array([[-1, -1, -1],
                   [-1, 8, -1],
                   [-1, -1, -1]])
                   
ridges = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)

cv2.imshow("Original", img)
cv2.imshow("Ridge Detection", ridges)
cv2.waitKey(0)

cv2.imwrite("ridges.jpg", ridges)
cv2.destroyAllWindows()