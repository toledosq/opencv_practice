import sys
import cv2

MAXSCALE = 100

scaleFactor = 1
windowName = "Resize Image"
trackbarValue = "Scale"

img = cv2.imread(sys.argv[1])

if img is None:
    print("Couldn't read", img)
    exit

# Create Window    
cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)

# Callback function
def scaleImage(*args):
    # Get the scale factor from the trackbar
    scaleFactor = 1 + args[0]/100.0
    # Resize the image
    scaledImage = cv2.resize(img, None, fx=scaleFactor, fy=scaleFactor, interpolation=cv2.INTER_LINEAR)
    cv2.imshow(windowName, scaledImage)

# Create trackbar and associate a callback function    
cv2.createTrackbar(trackbarValue, windowName, scaleFactor, MAXSCALE, scaleImage)

# Display the image
cv2.imshow(windowName, img)
cv2.waitKey(0)
cv2.destroyAllWindows()
