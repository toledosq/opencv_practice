import cv2
import matplotlib.pyplot as plt
import numpy as np

"""
Color spaces are an important concept in Computer Vision. Different lighting conditions can have an 
effect on color-based segmentation. Common problems in CV include skin tone detection, traffic 
light recognition, etc.

Color Spaces:

 - RGB
    * additive colorspace where colors are a linear combination of RGB
    * all three channels encode brightness as well as color
    * results in mixing of chrominance and luminance
    * non-uniformity between different lighting conditions
    
- LAB
    * contains 3 components:
        L = Lightness (Intensity)
        a = color component Green -> Magenta
        b = color component Blue -> Yellow
        
    * Two channels encode chrominance, one channel encodes brightness
    * Uniform color space approx to human color perception
    * Device-agnostic
    * Can be transformed to RGB
    
- YCrCb
    * Derived from RGB
    * Contains 3 components:
        Y = Luminance (Luma) obtained from RGB after gamma correction
        Cr = R - Y (how far is the red component from Luma)
        Cb = B - Y (how far is the blue component from Luma)
        
    * Two channels encode chrominance, one channel encodes luminance
    * Device-agnostic, mostly used in compression for TV Transmission
    
- HSV
    * Contains 3 components:
        H = Hue (Dominant Wavelength)
        S = Saturation
        V = Value (Intensity)
    * Only one channel descibes color (H)
    * Device-agnostic
    * Hue is represented as a circle, and red is at degree 0
    * That means red information may take the values [300,360] or [0,60]
"""


# Read in two pictures of a Rubik's cube, taken indoors and outdoors
indoors = cv2.imread('resources/color_spaces/indoors.png')
outdoors = cv2.imread('resources/color_spaces/outdoors.png')


# Show the color channels in RGB
B, G, R = cv2.split(indoors)
B_, G_, R_ = cv2.split(outdoors)

f, axarr = plt.subplots(1,4)

for idx, img in enumerate([indoors, B, G, R]):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    axarr[idx].axis('off')
    axarr[idx].imshow(img_rgb)

f_, axarr_ = plt.subplots(1,4)

for idx, img in enumerate([outdoors, B_, G_, R_]):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    axarr_[idx].axis('off')
    axarr_[idx].imshow(img_rgb)

plt.show()


### Using color spaces for segmentation ###

### RGB ###

# BGR of green taken from photo, +/- 40
bgr = [40, 158, 16]
thresh= 40

# Define min and max BGR values and place in array
min_bgr = np.array([bgr[0] - thresh, bgr[1] - thresh, bgr[2] - thresh])
max_bgr = np.array([bgr[0] + thresh, bgr[1] + thresh, bgr[2] + thresh])

# Create mask for green and apply to original image
mask_bgr = cv2.inRange(outdoors, min_bgr, max_bgr)
result_bgr = cv2.bitwise_and(outdoors, outdoors, mask=mask_bgr)


### HSV ###

# Convert BGR array to 3D, convert to HSV, capture first element
hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

# Define min/max HSV values and place in array
min_hsv = np.array([hsv[0] - thresh, hsv[1] - thresh, hsv[2] - thresh])
max_hsv = np.array([hsv[0] + thresh, hsv[1] + thresh, hsv[2] + thresh])

# Convert images to HSV colorspace
outdoors_hsv = cv2.cvtColor(outdoors, cv2.COLOR_BGR2HSV)
indoors_hsv = cv2.cvtColor(indoors, cv2.COLOR_BGR2HSV)

# Create mask and apply to original image
mask_hsv = cv2.inRange(outdoors_hsv, min_hsv, max_hsv)
result_hsv = cv2.bitwise_and(outdoors_hsv, outdoors_hsv, mask = mask_hsv)


### YCrCb ###

# Convert BGR array to 3D, convert to YCB, grab first element
ycb = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2YCrCb)[0][0]
min_ycb = np.array([ycb[0] - thresh, ycb[1] - thresh, ycb[2] - thresh])
max_ycb = np.array([ycb[0] + thresh, ycb[1] + thresh, ycb[2] - thresh])

# Convert original images to YCB colorspace
outdoors_ycb = cv2.cvtColor(outdoors, cv2.COLOR_BGR2YCrCb)
indoors_ycb = cv2.cvtColor(indoors, cv2.COLOR_BGR2YCrCb)

# Create mask and apply to original image
mask_ycb = cv2.inRange(outdoors_ycb, min_ycb, max_ycb)
result_ycb = cv2.bitwise_and(outdoors_ycb, outdoors_ycb, mask=mask_ycb)


# Convert BGR array to 3D, convert to LAB, grab first element
lab = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2LAB)[0][0]
min_lab = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
max_lab = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])

# Convert images to LAB color space
outdoors_lab = cv2.cvtColor(outdoors, cv2.COLOR_BGR2LAB)
indoors_lab = cv2.cvtColor(indoors, cv2.COLOR_BGR2LAB)

# Create a mask and apply to original image
mask_lab = cv2.inRange(outdoors_lab, min_lab, max_lab)
result_lab = cv2.bitwise_and(outdoors_lab, outdoors_lab, mask=mask_lab)


### Display Results ###
cv2.imshow("(BGR) Green isolated", result_bgr)
cv2.imshow("(HSV) Green isolated", result_hsv)
cv2.imshow("(YCB) Green isolated", result_ycb)
cv2.imshow("(LAB) Green isolated", result_lab)
cv2.waitKey(0)