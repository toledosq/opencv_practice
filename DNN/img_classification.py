"""
Resources -- https://learnopencv.com/deep-learning-with-opencvs-dnn-module-a-definitive-guide/
Caffe model and .prototxt -- https://github.com/shicai/DenseNet-Caffe/

Using Caffe and DenseNet169 for this one
"""

import sys
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help="path/to/image.jpg", required=True)
parser.add_argument('-m', '--model', help="Choose DenseNet ckpt (default: DenseNet121)", choices=['121', '161', '169', '201'], default='121')
parser.add_argument('-s', '--show', help="Number of results to show", type=lambda x: max(1, min(int(x), 5)), default=2)
args = parser.parse_args()

# Load input image
img = cv2.imread(args.input)

# Read in ImageNet class names
with open('config\classification_classes_ILSVRC2012.prototxt', 'r') as f:
    image_net_names = f.read().split('\n')
    
# Get just the first name of each class
class_names = [name.split(',')[0] for name in image_net_names]

# Load model weights
model = cv2.dnn.readNet(model=f'models/DenseNet_{args.model}.caffemodel', 
                        config=f'config/DenseNet_{args.model}.prototxt', 
                        framework='Caffe')
                        


# Create blob from image w/ DNN
# Note that blobFromImage places blob in list for you
blob = cv2.dnn.blobFromImage(image=img,
                             scalefactor=0.01,     # scale down image
                             size=(224,224),        # Ensure final size is 224x224
                             mean=(104, 117, 123))  # Mean val to subtract from RGB channels (normalize img)
                             

# Forward Propagate the input through the model
model.setInput(blob)
outputs = model.forward()
final_outputs = outputs[0]  # Just get the first

# Convert to 1D array
final_outputs = final_outputs.reshape(1000,1)  # One thousand rows for the one thousand labels

# Convert to softmax probabilities
probs = np.exp(final_outputs) / np.sum(np.exp(final_outputs))

# Flatten and sort the probabilities
probs = np.sort(probs.flatten())

# Get the highest confidence 
for i in range(1, args.show + 1):
    label_id = np.argsort(np.max(final_outputs, axis=1))[-i]
    final_prob = probs[-i] * 100

    # Map the label names
    result = class_names[label_id]

    # Label the image
    cv2.putText(img, f"{result} ({final_prob:.2f}%)", (25, 50*i), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


# Display results
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.imwrite('outputs/result_image.jpg', img)
