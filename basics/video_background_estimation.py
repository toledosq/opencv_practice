import sys
import cv2
import numpy as np

"""
Temporal Median Filtering

When estimating the background of data, there are two basic ways of doing so - finding the mean and finding the median

Using motion detection as an example, we should expect the image to stay relatively stable temporally. There might be some
small noise, which you can see in the first example below. However, motion will appear as a significant change in the image.

For example, imagine a camera watching a street. Every time a car goes by, there is a significant change in the image.
If you are averaging these frames, then as more cars pass by, their motion will start to get baked into the average value.
This can lead to less-than-optimal results, as the threshold for what is considered motion increases.

Or another problem, a slow moving object may fail to trigger motion detection, as with a reasonable sample time it will become part of the avg.

If you find the median background of the video, baking in will only happen if a car were stop moving for 50% of the sample time.
But if they aren't moving for 50% of the sample time, does it really count as motion?

For instance, the array [100, 101, 101, 100, 100, 100, 100, 101, 100] does not contain significant changes in value
It would be best to average the values to estimate the background level
Estimated background: ((100 * 9) + 3) / 9 = 100.3

However, in the array [100, 120, 100, 100, 100, 100, 120, 100, 100] we see significant changes in value
In this case it would be best to find the median value to estimate the background level
Estimated background: 100
Estimated background if averaged: ((100 * 9) + 40) / 9 = 104.4

"""

from skimage import data, filters

# Open Video
cap = cv2.VideoCapture(sys.argv[1])

# Randomely select 25 frames
frameIds = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=25)

# Store selected frames in an array
frames = []
for fid in frameIds:
    cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
    ret, frame = cap.read()
    frames.append(frame)
    
# Calculate the median along the time axis
medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)

# Display median frame
cv2.imshow('frame', medianFrame)
cv2.waitKey(0)
cv2.destroyAllWindows()


""" 
Motion Masking
"""

# Move ptr to beginning of video
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# Convert background to grayscale
medianFrame_gray = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)

# Loop over frames
ret = True
while(ret):
    # Read frame
    ret, frame = cap.read()
    
    # Convert to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Calculate abs diff of current frame and median frame
    dframe = cv2.absdiff(frame, medianFrame_gray)
    
    # Binary threshold
    th, dframe = cv2.threshold(dframe, 30, 255, cv2.THRESH_BINARY)
    
    # Display image
    cv2.imshow('frame', dframe)
    cv2.waitKey(20)
    
# Release video
cap.release()
cv2.destroyAllWindows()
