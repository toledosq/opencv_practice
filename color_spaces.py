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