
"""
Object Detection with OpenCV DNN

Resources: https://learnopencv.com/deep-learning-with-opencvs-dnn-module-a-definitive-guide/
MS COCO: https://cocodataset.org/#home
OpenCV SSD MobileNet: https://github.com/ChiekoN/OpenCV_SSD_MobileNet

Using MobileNet SSD (Single Shot Detector) trained on MS COCO dataset (TensorFlow)
"""

import sys
import cv2
import numpy as np
import argparse
from time import time

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='path/to/video.mp4', default='input/detect_test.mp4')
parser.add_argument('-s', '--show', help='how many boxed objects to show', default=5)
args = parser.parse_args()


# Capture video
cap = cv2.VideoCapture(args.input)
frame_height = int(cap.get(3))
frame_width = int(cap.get(4))

# Create video writer
out = cv2.VideoWriter('vid_detect_result.mp4', 
                      cv2.VideoWriter_fourcc(*'mp4v'), 
                      30, 
                      (frame_width, frame_height))

# Load MS COCO class names
with open('config/object_detection_classes_coco.txt', 'r') as f:
    class_names = f.read().split('\n')
    
# get a different color array for each class
# Holds tuples w/ 3 ints for coloring bounding boxes
COLORS = np.random.uniform(0, 255, size=(len(class_names), 3))

# Load model weights
model = cv2.dnn.readNet(model='models/frozen_inference_graph.pb',
                        config='config/ssd_mobilenet_v2_coco_2018_03_29.pbtxt',
                        framework='TensorFlow')

# Loop over frames
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # Get image from frame
        image = frame
        height, width, _ = image.shape

        # Create blob from image
        blob = cv2.dnn.blobFromImage(image=image, 
                                     size=(300,300),      # ensure img is 300x300 for TF
                                     mean=(104,117,123),  # standard mean for RGB
                                     swapRB=True)
                                     
        # Pass blob to model and forward propogate the blob through the model
        start = time()
        model.setInput(blob)
        output = model.forward() 
        end = time()
        fps = 1 / (end - start)

        # Loop over each detection
        # Output format: [[[[classLabel, confidenceScore, boundBoxX, boundBoxY, boundBoxWidth, boundBoxHeight]]]]
        for detection in output[0, 0, :args.show, :]:   # args.show 5 results by default
            # Get Confidence
            confidence = detection[2]
            
            # Draw bounding boxes
            if confidence > .4:       
                class_id = detection[1]  # Get class label
                class_name = class_names[int(class_id)-1]  # map class id to the class        
                
                # Pick random color 
                color = COLORS[int(class_id)]
                
                # Get Bounding Box coords and size
                box_x = int(detection[3] * width)
                box_y = int(detection[4] * height)
                box_w = int(detection[5] * width)
                box_h = int(detection[6] * height)
                
                # Draw box
                cv2.rectangle(image, 
                              (box_x, box_y), 
                              (box_w, box_h), 
                              color, 2)
                
                # Put class label on top of box
                cv2.putText(image, 
                            class_name, 
                            (box_x, box_y - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, color, 2)
                            
                # Put fps on top of frame
                cv2.putText(image,
                            f"FPS: {fps:.2f}",
                            (20, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (0, 255, 0), 2)
                    
        # Display Image
        cv2.imshow('image', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break
        
cap.release()
cv2.destroyAllWindows()
