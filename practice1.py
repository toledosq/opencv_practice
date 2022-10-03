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
        print(f'Error opening file {vid}')
    else:
        # Capture frame rate
        fps = vid_capture.get(cv2.CAP_PROP_FPS)
        
        # Capture frame count
        frame_count = vid_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        
        print(f'File {vid} opened successfully')
        print(f'Detected FPS: {fps}')
        print(f'Frame Count: {frame_count}')
        
    return vid_capture, fps
    
    
def display_video_frames(vid_capture, fps):
    # Set MS delay between frames
    delay = int(1000 / fps)
    
    # Set frame index to 0
    vid_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    # Loop through frames and display
    while vid_capture.isOpened():
        ret, frame = vid_capture.read()
        if ret:
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(delay)
            
            # User can exit early by hitting q
            if key == ord('q'):
                break
        else:
            break
    
    cv2.destroyAllWindows()
    
    
def write_frames_as_video(vid_capture, output_path, fps, frame_size):
    # Create output object
    output = cv2.VideoWriter(output_path, 
                            cv2.VideoWriter_fourcc('M','J','P','G'),    # Codec
                            fps, 
                            frame_size
                            )
    
    # Set frame index to 0
    vid_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    print(f'Writing video to {output_path}')
    
    # Loop through frames and write to disk
    while vid_capture.isOpened():
        ret, frame = vid_capture.read()
        if ret:
            output.write(frame)
        else:
            print('Done')
            break
            
    # Release lock on output video
    output.release()


if __name__ == '__main__':

    ### Image Basics ###

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
    
    ### Video Basics ###
    
    # Read an mp4 and display the frames
    vid_capture, fps = read_video('vid.mp4')
    display_video_frames(vid_capture, fps)
    
    # Release lock on video file
    vid_capture.release()
    del vid_capture
    
    # Read a folder of frames and display them
    frames_path = 'original_frames/%04d.png'
    vid_capture, fps = read_video(frames_path)
    if fps == 1:
        fps = 30
        print("FPS changed to 30")
    display_video_frames(vid_capture, fps)
    
    # Obtain frame size info
    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))
    frame_size = (frame_width, frame_height)
    
    # Save the frames as a video
    output_path = 'vid_from_frames.avi'
    write_frames_as_video(vid_capture, output_path, fps, frame_size)
    
    # Release lock on video file
    vid_capture.release()
    