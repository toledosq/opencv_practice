import sys
import cv2
import numpy as np
import win32gui, win32ui, win32con
from time import time


class WindowCapture:

    w = 0
    h = 0
    hwnd = 0
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    
    
    def __init__(self, window_name=None):
        # find the handle for the window
        # if none provided, capture desktop
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception(f'Window not found: {window_name}')
            
        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        
        if window_name is not None:
            # remove border
            border_pix = 8
            titlebar_pix = 30
            self.w -= border_pix * 2
            self.h -= titlebar_pix - border_pix
            self.cropped_x = border_pix
            self.cropped_y = titlebar_pix
        
            # Set the cropped coordinates offset so we can translate screenshot
            self.offset_x = window_rect[0] + self.cropped_x
            self.offset_y = window_rect[1] + self.cropped_y
        
        
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
        
    
    def get_screenshot(self):        
        # Get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
        
        # Convert raw data to format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')  # uint8
        img.shape = (self.h, self.w, 4)   # 4 channels
        
        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        
        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]
        
        # Make image C_CONTIGUOUS to avoid errors w/ cv.rectangle()
        img = np.ascontiguousarray(img)
        
        return img


    def test_get_screenshot(self):  
        # Get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
        
        # Save img as bitmap
        dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        
        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        
        print("Screenshot saved as debug.bmp")
        
        
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 1:
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)
        exit()

    wincap = WindowCapture(sys.argv[1])
    loop_time = time()
    c = 0
    while (True):
        screenshot = wincap.get_screenshot()
        
        cv2.imshow('Computer Vision', screenshot)
        
        if c >= 10:
            print(f'FPS {1 / (time() - loop_time)}')
            c = 0
        
        c += 1
        loop_time = time()
        
        # press q to exit
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
