import cv2
import numpy as np


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


def show_img(img, title):
    # Display image in a window and wait for user
    cv2.imshow(title, img)
    cv2.waitKey(0)

    # Destroy window
    cv2.destroyAllWindows()
    
    
def resize_img(img, scale_factor, interpolation_method=cv2.INTER_LINEAR):
    h,w,c = img.shape
    print(f'Original size: {h}x{w}')
    
    resized_img = cv2.resize(img, 
                             None,  # No custom hw provided
                             fx=scale_factor, 
                             fy=scale_factor, 
                             interpolation=interpolation_method
                             )
    return resized_img
    
    
def crop_img(img, left=0, right=0, top=0, bottom=0):
    print(f"Original shape: {img.shape}")
    
    img_height = img.shape[0] - 1
    img_width = img.shape[1] - 1

    # (height, width, channels)
    from_left = clamp(left, 0, img_width)
    from_right = clamp(img_width - right, 0, img_width)
    from_top = clamp(top, 0, img_height)
    from_bottom = clamp(img_height - bottom, 0, img_height)
    
    cropped_img = img[from_top:from_bottom, from_left:from_right]
        
    print(f"Cropped shape: {cropped_img.shape}")
    return cropped_img
    
    
def crop_img_center(img, shape: tuple):
    # Crops to new dimensions from center
    print(f"Original shape: {img.shape}")
    
    orig_y1 = img.shape[0]
    orig_x1 = img.shape[1]
    
    y_diff = int((orig_y1 - shape[0]) / 2)
    x_diff = int((orig_x1 - shape[1]) / 2)
    
    print("y_diff", y_diff)
    print("x_diff", x_diff)
    
    y0 = clamp(0 + y_diff, 0, orig_y1 - 1)
    y1 = clamp(orig_y1 - y_diff, 0, orig_y1 - 1)
    
    x0 = clamp(0 + x_diff, 0, orig_x1 - 1)
    x1 = clamp(orig_x1 - x_diff, 0, orig_x1 - 1)
    
    cropped_img = img[y0:y1, x0:x1]
    print(f"Center Cropped Shape: {cropped_img.shape}")
    
    return cropped_img


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
    
    
def write_frames_as_video(vid_capture, output_path, fps):
    
    # Obtain frame size info
    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))
    frame_size = (frame_width, frame_height)
    
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
    show_img(img, 'img.jpg')
    cv2.imwrite('img_copy.jpg', img)

    # Read, display, and save image as grayscale
    # img_grayscale = cv2.imread('img.jpg', cv2.IMREAD_GRAYSCALE)
    # show_img(img_grayscale, 'Grayscale Image')
    # cv2.imwrite('img_grayscale.jpg', img_grayscale)
    
    # Resize and save an image
    # downscale_factor = 0.5
    # img_downscaled = resize_img(img, downscale_factor)
    # show_img(img_downscaled, 'Downscaled Image')
    # cv2.imwrite('img_downscaled.jpg', img_downscaled)
    
    # upscale_factor = 2
    # img_upscaled = resize_img(img, upscale_factor)
    # show_img(img_upscaled, 'Upscaled Image')
    # cv2.imwrite('img_upscaled.jpg', img_upscaled)
    
    # Crop an image
    img_cropped = crop_img(img, left=256, right=256, top=85, bottom=85)
    show_img(img_cropped, 'Cropped Image')
    
    # Crop an image by providing new shape
    img_center_cropped = crop_img_center(img, shape=(512,512))
    show_img(img_center_cropped, 'Center Cropped Image')
    
    
    ### Video Basics ###
    
    # Read an mp4 and display the frames
    # vid_capture, fps = read_video('vid.mp4')
    # display_video_frames(vid_capture, fps)
    
    # Release lock on video file
    # vid_capture.release()
    # del vid_capture
    
    # Read a folder of frames and display them
    # frames_path = 'original_frames/%04d.png'
    # vid_capture, fps = read_video(frames_path)
    # if fps == 1:
        # fps = 30
        # print("FPS changed to 30")
    # display_video_frames(vid_capture, fps)
    
    # Save the frames as a video
    # output_path = 'vid_from_frames.avi'
    # write_frames_as_video(vid_capture, output_path, fps)
    
    # Release lock on video file
    # vid_capture.release()
    