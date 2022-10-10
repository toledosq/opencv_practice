import sys
import cv2
import numpy as np
import win32gui, win32ui, win32con
from time import time


class WC:

    w = 0
    h = 0
    hwnd = 0
    cx = 0
    cy = 0
    ox = 0
    oy = 0
    
    
    def __init__(self, w):
        self.hwnd = win32gui.FindWindow(None, w)
        if not self.hwnd:
            raise Exception(f'Window not found: {w}')            
        wr = win32gui.GetWindowRect(self.hwnd)
        self.w = wr[2] - wr[0]
        self.h = wr[3] - wr[1]
        bpx = 8
        tpx = 30
        self.w -= bpx * 2
        self.h -= tpx - bpx
        self.cx = bpx
        self.cy = tpx
        self.ox = wr[0] + self.cx
        self.oy = wr[1] + self.cy
        
        
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
        
    
    def get_screen(self):        
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dBMap = win32ui.CreateBitmap()
        dBMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dBMap)
        
        cDC.BitBlt((0,0), (self.w, self.h), dcObj, (self.cx, self.cy), win32con.SRCCOPY)
        sInts = dBMap.GetBitmapBits(True)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dBMap.GetHandle())

        img = np.fromstring(sInts, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        img = img[...,:3]
        img = np.ascontiguousarray(img)
        
        return img
        
        
    def find_objs(self, t=0.5, cmp=cv2.TM_CCOEFF_NORMED):
        img_ = img.copy()
        hmap = cv2.matchTemplate(img_, obj_img, cmp)

        l = list(zip(*(np.where(hmap >= t))[::-1]))
        r = []

        if l:
            ow = o_img.shape[1]
            oh = o_img.shape[0]

            for loc in l[:10]:
                tl = loc
                br = (tl[0] + ow, tl[1] + oh)
                r.append([int(loc[0]), int(loc[1]), ow, oh])
                
            r, _ = cv2.groupRectangles(r, 1, 0.5)
            
            pts = []
            if len(r):
                for (x, y, w, h) in r:
                    cx = x + int(w/2)
                    cy = y + int(h/2)
                    pts.append((cx, cy))

                    cv2.drawMarker(img, 
                                   (cx, cy), 
                                   (255, 0, 255), 
                                   markerType=3, 
                                   markerSize=40, 
                                   thickness=2)


    def test_get_screen(self):  
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dBMap = win32ui.CreateBitmap()
        dBMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dBMap)
        cDC.BitBlt((0,0), (self.w, self.h), dcObj, (self.cx, self.cy), win32con.SRCCOPY)

        dBMap.SaveBitmapFile(cDC, 'debug.bmp')
        
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dBMap.GetHandle())


if __name__ == '__main__':
    wincap = WC(sys.argv[1])
    lt = time()
    c = 0
    while (True):
        cv2.imshow('', wincap.get_screen())
        
        if c >= 10:
            print(f'FPS {1 / (time() - lt)}')
            c = 0

        c += 1
        lt = time()

        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
