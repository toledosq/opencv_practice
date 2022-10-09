import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


src = cv2.imread("threshold.png", cv2.IMREAD_GRAYSCALE)
src_rgb = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
fig, axes = plt.subplots(5, 4, figsize=(12, 15))
fig.tight_layout()
for i in range(0,5):
    axes[i][0].axis('off')
    axes[i][0].set_title("Original")
    axes[i][0].imshow(src_rgb)


""" 
Binary thresholding

> if src(x,y) > thresh
>   dst(x,y) = maxValue
> else
>   dst(x,y) = 0

cv2.THRESH_BINARY
"""

# (threshold, maxValue)
tm = [(0, 255),
      (127, 255),
      (127, 128)]
      
for i, tm_ in enumerate(tm, 1):
    th, dst = cv2.threshold(src, tm_[0], tm_[1], cv2.THRESH_BINARY)
    rgb_img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    axes[0][i].axis('off')
    axes[0][i].set_title(f"Binary (t={tm_[0]}, m={tm_[1]})")
    axes[0][i].imshow(rgb_img)
    
    
"""
Inverse-Binary Thresholding

if src(x,y) > thresh
  dst(x,y) = 0
else
  dst(x,y) = maxValue
  
cv2.THRESH_BINARY_INV
"""
tm = [(0, 255),
      (127, 255),
      (127, 128)]
      
for i, tm_ in enumerate(tm, 1):
    th, dst = cv2.threshold(src, tm_[0], tm_[1], cv2.THRESH_BINARY_INV)
    rgb_img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    axes[1][i].axis('off')
    axes[1][i].set_title(f"Inverse Binary (t={tm_[0]}, m={tm_[1]})")
    axes[1][i].imshow(rgb_img)


"""
Truncate Thresholding

if src(x,y) > thresh
  dst(x,y) = thresh
else
  dst(x,y) = src(x,y)
  
cv2.THRESH_TRUNC
maxValue ignored
"""

tm = [(0, 255),
      (127, 255),
      (64, 128)]
      
for i, tm_ in enumerate(tm, 1):
    th, dst = cv2.threshold(src, tm_[0], tm_[1], cv2.THRESH_TRUNC)
    rgb_img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    axes[2][i].axis('off')
    axes[2][i].set_title(f"Truncate (t={tm_[0]}, m={tm_[1]})")
    axes[2][i].imshow(rgb_img)
    
    
"""
Threshold to Zero

if src(x,y) > thresh:
    dst(x,y) = src(x,y)
else:
    dst(x,y) = 0
    
cv2.THRESH_TOZERO
"""

tm = [(0, 255),
      (127, 255),
      (64, 255)]
      
for i, tm_ in enumerate(tm, 1):
    th, dst = cv2.threshold(src, tm_[0], tm_[1], cv2.THRESH_TOZERO)
    rgb_img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    axes[3][i].axis('off')
    axes[3][i].set_title(f"Thresh to Zero (t={tm_[0]}, m={tm_[1]})")
    axes[3][i].imshow(rgb_img)


"""
Inverted Threshold to Zero

if src(x,y) > thresh:
    dst(x,y) = src(x,y)
else:
    dst(x,y) = 0
    
cv2.THRESH_TOZERO_INV
"""

tm = [(0, 255),
      (127, 255),
      (196, 255)]
      
for i, tm_ in enumerate(tm, 1):
    th, dst = cv2.threshold(src, tm_[0], tm_[1], cv2.THRESH_TOZERO_INV)
    rgb_img = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    axes[4][i].axis('off')
    axes[4][i].set_title(f"Inverse T20 (t={tm_[0]}, m={tm_[1]})")
    axes[4][i].imshow(rgb_img)
    

plt.show()
