import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file', help='path/to/file.jpg', 
                                    required=True, 
                                    type=str)
                                    
parser.add_argument('-i', '--isolate', help='Isolate a color', 
                                       action='store_true')
                                    
parser.add_argument('-m', '--mask', help='Specify \"R,G,B\" mask for color isolation',
                                    type=str,
                                    default='')
                                    
parser.add_argument('-t', '--thresh', help='Set color threshold (ie +/- 50)', 
                                      type=int, 
                                      default=40)
args = parser.parse_args()


def read_img(imgPath):
    try:
        img = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)
    except Exception as e:
        print(e)
        return None
    else:
        return img


def isolate_color(img, bgr, thresh, cs_convert):
    color_array = cv2.cvtColor(np.uint8([[bgr]]), cs_convert)[0][0]

    thresh_min = np.array([(color_array[0] - thresh), 
                           (color_array[1] - thresh), 
                           (color_array[2] - thresh)
                         ])
                         
    thresh_max = np.array([(color_array[0] + thresh), 
                           (color_array[1] + thresh), 
                           (color_array[2] + thresh)
                         ])
    
    if cs_convert == cv2.COLOR_BGR2RGB:
        thresh_min = thresh_min.clip(min=0, max=255)
        thresh_max = thresh_max.clip(min=0, max=255)
        
    print(f"Shape of color_array: {color_array}")
    print(f"Shape of thresh_min: {thresh_min}")
    print(f"Shape of thresh_max: {thresh_max}")
    
    mask = cv2.inRange(img, thresh_min, thresh_max)
    result = cv2.bitwise_and(img, img, mask=mask)
    
    return result
    

if __name__ == '__main__':
    # Read image into memory
    img = read_img(args.file)
    
    # Convert images to other color spaces
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    ycb_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Add results to output list
    output_images = [rgb_img, hsv_img, ycb_img, lab_img]
    
    # Set ImageGrid size
    image_grid_size = (1, 4)
    
    # Get isolated color images
    if args.isolate:
        # Show color selection window
        if args.mask == '':
            import tkinter as tk
            import tkinter.ttk as ttk
            from tkcolorpicker import askcolor

            root = tk.Tk()
            style = ttk.Style(root)
            style.theme_use('clam')

            isolated_bgr = np.array(list(askcolor((255, 255, 0), root)[0])[::-1])
            root.destroy()
        else:
            isolated_bgr = np.array([int(y.strip()) for y in args.mask.split(',')])[::-1]
            
        print(f"isolated_bgr:", isolated_bgr)
        
        isolated_rgb_img = isolate_color(rgb_img, isolated_bgr, args.thresh, cs_convert=cv2.COLOR_BGR2RGB)
        isolated_hsv_img = cv2.cvtColor(isolate_color(hsv_img, isolated_bgr, args.thresh, cs_convert=cv2.COLOR_BGR2HSV), cv2.COLOR_HSV2RGB)
        isolated_ycb_img = cv2.cvtColor(isolate_color(ycb_img, isolated_bgr, args.thresh, cs_convert=cv2.COLOR_BGR2YCrCb), cv2.COLOR_YCrCb2RGB)
        isolated_lab_img = cv2.cvtColor(isolate_color(lab_img, isolated_bgr, args.thresh, cs_convert=cv2.COLOR_BGR2LAB), cv2.COLOR_LAB2RGB)
        
        # Add isolated color images to output row
        output_images.extend([isolated_rgb_img, isolated_hsv_img, isolated_ycb_img, isolated_lab_img])
        
        # Add another row to image grid
        image_grid_size = (2, 4)
    
    # Create plot
    fig = plt.figure(figsize=(10., 4.))
    grid = ImageGrid(fig, 111,
                     nrows_ncols=image_grid_size, 
                     axes_pad=0.1
                    )
    
    # Populate plot
    for ax, im in zip(grid, output_images):
        ax.axis('off')
        ax.imshow(im)
        
    # Show plot
    plt.show()
    