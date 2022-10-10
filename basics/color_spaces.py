import cv2
import matplotlib as mpl
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


# Read in picture
input_img = cv2.imread('resources/color_spaces/outdoors.png')


# Split color channels in RGB
B, G, R = cv2.split(input_img)

fig, axes = plt.subplots(1,4, figsize=(12, 4))
for idx, img in enumerate([input_img, B, G, R]):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    axes[idx].axis('off')
    axes[idx].imshow(img_rgb)
    

### Using color spaces for segmentation ###

### RGB ###

# BGR of taken from img, +/- thresh based on histogram
bgr = [40, 158, 16]
thresh=30

# Define min and max BGR values and place in array
min_bgr = np.array([bgr[0] - thresh, bgr[1] - thresh, bgr[2] - thresh])
max_bgr = np.array([bgr[0] + thresh, bgr[1] + thresh, bgr[2] + thresh])

# Create mask for green and apply to original image
mask_bgr = cv2.inRange(input_img, min_bgr, max_bgr)
result_bgr = cv2.bitwise_and(input_img, input_img, mask=mask_bgr)


### HSV ###

# Convert BGR array to 3D, convert to HSV, capture first element
hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

# Define min/max HSV values and place in array
min_hsv = np.array([hsv[0] - thresh, hsv[1] - thresh, hsv[2] - thresh])
max_hsv = np.array([hsv[0] + thresh, hsv[1] + thresh, hsv[2] + thresh])

# Convert images to HSV colorspace
input_img_hsv = cv2.cvtColor(input_img, cv2.COLOR_BGR2HSV)

# Create mask and apply to original image
mask_hsv = cv2.inRange(input_img_hsv, min_hsv, max_hsv)
result_hsv = cv2.bitwise_and(input_img_hsv, input_img_hsv, mask = mask_hsv)


### YCrCb ###

# Convert BGR array to 3D, convert to YCB, grab first element
ycb = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2YCrCb)[0][0]
min_ycb = np.array([ycb[0] - thresh, ycb[1] - thresh, ycb[2] - thresh])
max_ycb = np.array([ycb[0] + thresh, ycb[1] + thresh, ycb[2] - thresh])

# Convert original images to YCB colorspace
input_img_ycb = cv2.cvtColor(input_img, cv2.COLOR_BGR2YCrCb)

# Create mask and apply to original image
mask_ycb = cv2.inRange(input_img_ycb, min_ycb, max_ycb)
result_ycb = cv2.bitwise_and(input_img_ycb, input_img_ycb, mask=mask_ycb)


# Convert BGR array to 3D, convert to LAB, grab first element
lab = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2LAB)[0][0]
min_lab = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
max_lab = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])

# Convert images to LAB color space
input_img_lab = cv2.cvtColor(input_img, cv2.COLOR_BGR2LAB)

# Create a mask and apply to original image
mask_lab = cv2.inRange(input_img_lab, min_lab, max_lab)
result_lab = cv2.bitwise_and(input_img_lab, input_img_lab, mask=mask_lab)


### Display Results ###
fig1, axes1 = plt.subplots(1,5, figsize=(20,4))
for idx, result in enumerate([input_img, result_bgr, result_hsv, result_ycb, result_lab]):
    img_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    axes1[idx].axis('off')
    axes1[idx].imshow(img_rgb)
    
axes1[0].set_title('Original')
axes1[1].set_title('RGB')
axes1[2].set_title('HSV')
axes1[3].set_title('YCrCb')
axes1[4].set_title('LAB')

# plt.show()


### Compute Density Plots for isolated color###

im = result_bgr

# Separate channels and create arrays (BGR)
B = np.array([])
G = np.array([])
R = np.array([])

b = im[:,:,0]
b = b.reshape(b.shape[0]*b.shape[1])
g = im[:,:,1]
g = g.reshape(g.shape[0]*g.shape[1])
r = im[:,:,2]
r = r.reshape(r.shape[0]*r.shape[1])

B = np.append(B,b)
G = np.append(G,g)
R = np.append(R,r)


# Create Density plots
nbins = 10
fig2, axes2 = plt.subplots(1,3, figsize=(12,4))
fig2.tight_layout()

# B -> G
axes2[0].hist2d(B, G, bins=nbins, norm=mpl.colors.LogNorm())
axes2[0].set_title('RGB')
axes2[0].set_xlabel('B')
axes2[0].set_ylabel('G')
axes2[0].set_xlim([0,255])
axes2[0].set_ylim([0,255])

# B -> R
axes2[1].hist2d(B, R, bins=nbins, norm=mpl.colors.LogNorm())
axes2[1].set_title('RGB')
axes2[1].set_xlabel('B')
axes2[1].set_ylabel('R')
axes2[1].set_xlim([0,255])
axes2[1].set_ylim([0,255])

# R -> G
axes2[2].hist2d(R, G, bins=nbins, norm=mpl.colors.LogNorm())
axes2[2].set_title('RGB')
axes2[2].set_xlabel('R')
axes2[2].set_ylabel('G')
axes2[2].set_xlim([0,255])
axes2[2].set_ylim([0,255])


plt.show()


# 