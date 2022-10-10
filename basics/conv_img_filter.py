import cv2
import numpy as np


"""
Convolution Kernels are a FUNDAMENTAL processing technique in CV

In image processing, a Convolution Kernel is a 2D matrix used to filter image. 
AKA Convolution Matrix

MxN matrix, where M, N are odd integers 
typically square (e.g. 3x3, 5x5, 7x7, etc.)

These Convolution Kernels can be used to perform ops on each pixel of an image.

The cv2.filter2D(src, ddepth, kernel) function is used to apply kernels
- ddepth refers to the depth of the resulting image, -1 will preserve original depth
"""

"""
Applying Identity Kernel

The identity Kernel is a square matrix where middle element is 1, and all other elements 0
Multiplying it with any other matrix will return the original matrix.

Applying this kernel to an image will leave it unchanged.
"""

image = cv2.imread('img.jpg')
if image is None:
    print("Could not read image")
    exit
    
# Apply identity kernel
kernel1 = np.array([[0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0]])
                    
identity = cv2.filter2D(src=image, ddepth=-1, kernel=kernel1)

cv2.imshow('Original', image)
cv2.imshow('Identity', identity)
cv2.waitKey(0)

cv2.imwrite('identity.jpg', identity)
cv2.destroyAllWindows()


"""
Blurring images (uniform avg)

1. Assume that the center of the kernel is positioned over a specific pixel (p) in an image
2. Multiply the value of each element in the kernel with the corresponding pixel element
3. Sum the result of those multiplications and compute the average
4. Replace the value of pixel (p) with the average

Repeat for every pixel in the source image.
"""

# Create a 5x5 matrix of ones with full precision and normalize 
# (divide each element by total num of elements in kernel)
kernel2 = np.ones((5, 5), np.float32) / 25
print(kernel2)

# Apply blur kernel to source image
blurred = cv2.filter2D(src=image, ddepth=-1, kernel=kernel2)

# Or using the built-in method
blurred_builtin = cv2.blur(src=image, ksize=(5,5))

# Show user
cv2.imshow('Original', image)
cv2.imshow('Kernel Blur', blurred)
cv2.imshow('Kernel Blur', blurred_builtin)
cv2.waitKey(0)

# Write to disk
cv2.imwrite('blur_kernel.jpg', blurred)
cv2.destroyAllWindows()


"""
Other types of blurring
"""

# Gaussian Blur
gaussian_blur = cv2.GaussianBlur(src=image,     
                                 ksize=(5,5),   # Kernel Size
                                 sigmaX=0,      # horizontal std deviation
                                 sigmaY=0)      # vertical std deviation
                                 

# Median Blur
median_blur = cv2.medianBlur(src=image, ksize=5)

# Bilateral Filter (Gaussian + ridge detection)
bilateral_filter = cv2.bilateralFilter(src=image,
                                       d=7,             # pixel neighborhood diameter
                                       sigmaColor=0,    # pixel intensity delta tolerance
                                       sigmaSpace=0)    # spatial extent of kernel

cv2.imshow('Original', image)
cv2.imshow('Gaussian Blurred', gaussian_blur)
cv2.imshow('Median Blurred', median_blur)
cv2.imshow('Bilateral Filtering', bilateral_filter)
cv2.waitKey(0)

cv2.imwrite('gaussian_blur.jpg', gaussian_blur)
cv2.imwrite('median_blur.jpg', median_blur)
cv2.imwrite('bilateral_filter.jpg', bilateral_filter)
cv2.destroyAllWindows()