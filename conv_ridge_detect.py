import sys, os
import cv2
import numpy as np

image_path = sys.argv[1]
print(image_path)

img = cv2.imread(sys.argv[1], 0)  # Read in as grayscale

size = (img.shape[1], img.shape[0])
preview_size = (960, 540)
if img is None:
    print('Could not read image', sys.argv[1])

# Resize img if too big
print(f'Img Resolution: {size[0]}x{size[1]}')
print(f'Preview Resolution: {preview_size[1]}x{preview_size[0]}')
if size[0] > preview_size[0] or size[1] > preview_size[1]:
    img = cv2.resize(img,(0,0),fx=(preview_size[0] / img.shape[1]),
                               fy=(preview_size[1] / img.shape[0]),
                               interpolation=cv2.INTER_AREA)
    
kernel = np.array([[-1, -1, -1],
                   [-1, 8, -1],
                   [-1, -1, -1]], np.float32)

# Blur image for better detection
blurred_img = cv2.GaussianBlur(src=img, ksize=(3,3), sigmaX=0, sigmaY=0)

ridges = cv2.filter2D(src=blurred_img, ddepth=-1, kernel=kernel)

cv2.imshow("Original", img)
cv2.imshow("Ridge Detection", ridges)
cv2.waitKey(0)

# cv2.imwrite("ridges.jpg", ridges)
cv2.destroyAllWindows()