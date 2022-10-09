import sys
import cv2
import numpy as np
from basics import crop_img

"""
Sobel Edge detection

Edges can be detected in areas where the Pixel Intensity gradient is higher than a particular threshold value
In addition, a sudden change in the derivative will reveal a change in Pixel Intensity
We can approximate the derivative w/ a 3x3 Kernel

We use two convolutional kernels, X-Direction and Y-Direction, to detect sudden changes in pixel intensity

X-Direction
[[-1, 0, 1],
 [-2, 0, 2],
 [-1, 0, 1]]

Y-Direction
[[ 1,  2,  1],
 [ 0,  0,  0]
 [-1, -2, -1]

Convolving with only the horizontal kernel yields a Sobel img w/ edges enhanced in X-direction
Convolving with only the vertical kernel yields a Sobel img w/ edges enhanced in Y-direction

Let A = X-Direction Kernel
Let B = Y-Direction Kernel
Let I = Source Image
Let * = Convolution Operator
Let Gx = A * I (Gradient Intensity in X-Direction)
Let Gy = B * I (Gradient Intensity in Y-Direction)
Let G = The final approximation of Gradient Magnitude

Gradient Magnitude = sqrt( (Gx ** 2) * (Gy ** 2) )
Gradient Orientation = arctan(Gy / Gx)

Function syntax: cv2.Sobel(src, ddepth, dx, dy)
where ddepth = precision
dx, dy = derivative order in each direction
"""


img = cv2.imread(sys.argv[1], 0)  # Read in as grayscale
size = (img.shape[1], img.shape[0])
preview_size = (960, 540)
if img is None:
    print('Could not read image', sys.argv[1])

# Resize img if too big
print(f'Img Resolution: {size[0]}x{size[1]}')
if size[0] > preview_size[0] or size[1] > preview_size[1]:
    img = cv2.resize(img,(0,0),fx=(preview_size[0] / img.shape[1]),
                               fy=(preview_size[1] / img.shape[0]),
                               interpolation=cv2.INTER_AREA)

# Blur img w/ 3x3 kernel for better edge detection
img_blur = cv2.GaussianBlur(img, (3,3), sigmaX=0, sigmaY=0)

# Sobel Edge Detection
sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)  # X-Axis
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)  # Y-Axis
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)  # X and Y

cv2.imshow('Sobel X', sobelx)
cv2.imshow('Sobel Y', sobely)
cv2.imshow('Sobel X and Y', sobelxy)
cv2.waitKey(0)
cv2.destroyAllWindows()


"""
Canny Edge Detection

1. Noise Reduction
2. Calculating Intensity Gradient of the Image
3. Suppression of False Edges
4. Hysteresis Thresholding
"""