import sys
import cv2


# Lists to store the bounding box coordinates
top_left_corner = []
bottom_right_corner = []

# Callback function
def drawRectangle(action, x, y, flags, *userdata):
    global top_left_corner, bottom_right_corner
    
    if action == cv2.EVENT_LBUTTONDOWN:  # On click
        top_left_corner = [(x, y)]
    elif action == cv2.EVENT_LBUTTONUP:  # On release
        bottom_right_corner = [(x, y)]
        cv2.rectangle(img, top_left_corner[0], bottom_right_corner[0], (0,255,0), 2, 8)
        cv2.imshow("Window", img)
        
img = cv2.imread(sys.argv[1])
if img is None:
    print("Could not read image", img)
    exit

temp = img.copy()  # for clearing annotation
cv2.namedWindow("Window")
cv2.setMouseCallback("Window", drawRectangle)

k=0
# Close the window when 'q' is pressed
while k!=113:
    cv2.imshow("Window", img)
    k = cv2.waitKey(0)
    
    # Clear window if 'c' is pressed
    if k == 99:
        img = temp.copy()
        cv2.imshow("Window", img)

cv2.destroyAllWindows()
