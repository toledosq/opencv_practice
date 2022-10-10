import sys, os
import cv2
import numpy as np


def find_objects(img, obj_img, threshold=0.5, comparison_algo=cv2.TM_CCOEFF_NORMED, debug_mode=False):
    if img is None:
        print("Could not read image", img)
        return None
    elif obj_img is None:
        print("Could not read image", obj_img)
        return None
        
    src_img = img.copy()

    # Find possible matches for object in screenshot
    result = cv2.matchTemplate(src_img, obj_img, comparison_algo)  # using TM_CCOEFF_NORMED as comparison algo

    # Get all matching objects
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    rectangles = []

    # Annotate matches
    if locations:
        print("Found matches")
        obj_w = obj_img.shape[1]
        obj_h = obj_img.shape[0]

        # Add all locations found to a list
        for loc in locations:
            top_left = loc
            bottom_right = (top_left[0] + obj_w, top_left[1] + obj_h)
            rectangles.append([int(loc[0]), int(loc[1]), obj_w, obj_h])
            
        # Group nearby locations
        rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        
        points = []
        if len(rectangles):
            for (x, y, w, h) in rectangles:
                # Find center point
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                
                # Save the points
                points.append((center_x, center_y))
                
                # Draw center point
                cv2.drawMarker(src_img, (center_x, center_y), color=(0, 255, 0), markerType=cv2.MARKER_TILTED_CROSS, markerSize=40, thickness=2)
        
              
        if debug_mode:
            cv2.imshow('Matches', src_img)
            cv2.waitKey()
            cv2.imwrite('outputs/debug_matches.jpg', src_img)


if __name__ == '__main__':
    src_img = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
    obj_img = cv2.imread(sys.argv[2], cv2.IMREAD_UNCHANGED)
    thresh = float(sys.argv[3])
    
    find_objects(src_img, obj_img, thresh, debug_mode=True)
