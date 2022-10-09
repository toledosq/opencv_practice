import os
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", help="path/to/image.jpg")
parser.add_argument('-f', '--folder', help="path/to/image/folder")
parser.add_argument('-s', '--size', help="Patch height,width in pixels")
args = parser.parse_args()

print(args.image, args.folder, args.size)


def read_img(imgPath):
    try:
        img = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)
    except Exception as e:
        raise
    else:
        return img
        

def divide_img(img, patch_size):
    print('Dividing image into patches of size', patch_size)
    
    image_copy = img.copy()

    imgheight = img.shape[0]
    imgwidth = img.shape[1]
    M = patch_size[0]
    N = patch_size[1]
    x1 = 0
    y1 = 0

    # Iterate through img array using patch size == step size
    for y in range(0, imgheight, M):
        for x in range(0, imgwidth, N):
            if (imgheight - y) < M or (imgwidth - x) < N:
                break
                
            y1 = y + M
            x1 = x + N

            # check if patch size exceeds img size
            if x1 >= imgwidth and y1 >= imgheight:
                x1 = imgwidth - 1
                y1 = imgheight - 1
            elif y1 >= imgheight: # when patch height exceeds the image height
                y1 = imgheight - 1
            elif x1 >= imgwidth: # when patch width exceeds the image width
                x1 = imgwidth - 1
                
            # Save each patch into file directory and draw rect on cv2 img (for visualization)
            tiles = image_copy[y:y+M, x:x+N]
            cv2.imwrite('./saved_patches/'+'tile'+str(x)+'_'+str(y)+'.jpg', tiles)
            cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)
            
    print('Done')
    return img


if __name__ == '__main__':
    images = [args.image]
    size = tuple([int(s) for s in args.size.split(',')])
    if args.folder is not None:
        if os.path.isdir(args.folder) and os.path.exists(args.folder):
            images.extend([os.path.join(args.folder, f) for f in os.listdir(args.folder) if f.endswith('.jpg')])

    print(len(images), 'images')
    print('Patch size:', size)
    
    for image in images:
        img = read_img(image)
        patched_img = divide_img(img, size)
        cv2.imshow('Patched image', patched_img)
        cv2.waitKey(0)
        
        cont = input("Press y to continue or any other key to exit: ")
        if cont.lower == 'y':
            break
