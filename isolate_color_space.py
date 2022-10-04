import cv2
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys, os

parser = argparse.ArgumentParser()
parser.add_argument('-hsv', help='Display HSV color space', action='store_true')
parser.add_argument('-ycb', help='Display YCB color space', action='store_true')
parser.add_argument('-lab', help='Display LAB color space', action='store_true')

parser.add_argument('-i', help='Isolate color by name', required=True,
                                                        choices=['red', 
                                                                 'violet', 
                                                                 'blue', 
                                                                 'cyan', 
                                                                 'green', 
                                                                 'yellow', 
                                                                 'orange', 
                                                                 'white', 
                                                                 'black'
                                                                 ])  ## Provide some basic color enums
                                                                 
parser.add_argument('-f', '--file', help='path/to/file.jpg', required=True, type=str)
parser.add_argument('-t', '--thresh', help='Set color threshold (ie +/- 50)', type=int)
args = parser.parse_args()


# Color BGR enumerations
colors_bgr = {'red':    [0  ,   0, 255],
              'violet': [255,   0, 255],
              'blue':   [255,   0,   0],
              'cyan':   [255, 255,   0],
              'green':  [0  , 255,   0],
              'yellow': [0  , 255, 255],
              'orange': [0  , 128, 255],
              'white':  [255, 255, 255],
              'black':  [0  , 0  ,   0]
             }
             
spaces = {'ycb': cv2.COLOR_BGR2YCrCb,
          'hsv': cv2.COLOR_BGR2HSV,
          'lab': cv2.COLOR_BGR2LAB,
          'rgb': cv2.COLOR_BGR2RGB
         }
             
isolate_bgr = colors_bgr[args.i]
thresh = args.thresh if args.thresh else 40


def read_img(imgPath):
    try:
        img = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)
    except Exception as e:
        print(e)
        return None
    else:
        return img


def isolate_color(img, bgr, thresh, color_space='bgr'):
    color_array = np.array(bgr) if color_space == 'bgr' else cv2.cvtColor(np.uint8([[bgr]]), spaces[color_space])[0][0]

    thresh_min = np.array([(color_array[0] - thresh), 
                           (color_array[1] - thresh), 
                           (color_array[2] - thresh)
                         ]).clip(min=0, max=255)
                         
    thresh_max = np.array([(color_array[0] + thresh), 
                           (color_array[1] + thresh), 
                           (color_array[2] + thresh)
                         ]).clip(min=0, max=255)
    
    print(f"Shape of color_array: {color_array}")
    print(f"Shape of thresh_min: {thresh_min}")
    print(f"Shape of thresh_max: {thresh_max}")
    
    mask = cv2.inRange(img, thresh_min, thresh_max)
    result = cv2.bitwise_and(img, img, mask=mask)
    
    return result
    

if __name__ == '__main__':
    # Read image into memory
    img = read_img(args.file)
    
    isolated_bgr_img = isolate_color(img, isolate_bgr, thresh)
    cv2.imshow(f"Isolated {args.i} (BGR)", isolated_bgr_img)
    cv2.waitKey(0)
