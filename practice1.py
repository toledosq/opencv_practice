import cv2


def show_img(img, outpath=None):
    # Display image in a window and wait for user
    cv2.imshow('Image', img)
    cv2.waitKey(0)

    # Destroy window
    cv2.destroyAllWindows()
    

def read_video(vid):
    vid_capture = cv2.VideoCapture(vid)
    
    if not vid_capture.isOpened():
        print(f"Error opening file {vid}")
    else:
        # Capture frame rate
        fps = vid_capture.get(cv2.CAP_PROP_FPS)
        
        # Capture frame count
        frame_count = vid_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        
        print(f"File {vid} opened successfully")
        print(f"Detected FPS: {fps}")
        print(f"Frame Count: {frame_count}")
        
    return vid_capture, fps
    
    
def display_video_frames(vid_capture, fps):
    delay = int(1000 / fps)
    while vid_capture.isOpened():
        ret, frame = vid_capture.read()
        if ret:
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(delay)
            
            if key == ord('q'):
                break
        else:
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':

    # Read, display, and save copy of image
    img = cv2.imread('img.jpg', cv2.IMREAD_UNCHANGED)
    show_img(img)
    cv2.imwrite('img_copy.jpg', img)

    # Read, display, and save image as grayscale
    img_grayscale = cv2.imread('img.jpg', cv2.IMREAD_GRAYSCALE)
    show_img(img_grayscale)
    cv2.imwrite('img_grayscale.jpg', img_grayscale)
    
    del img
    del img_grayscale
    
    # Video stuff
    vid, fps = read_video('vid.mp4')
    display_video_frames(vid, fps)
    vid.release()