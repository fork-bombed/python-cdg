import cv2
import numpy as np
from color import Color
import packet

WINDOW_NAME = 'CD+G'

class Window:
    def __init__(self,name):
        self.name = name
        self.previous = None
        self._create_window()
    def resize(self,width,height):
        cv2.resizeWindow(WINDOW_NAME,width,height)
    def wait(self):
        cv2.waitKey(0)
    def update(self,img):
        cv2.imshow(WINDOW_NAME, img)
        self.previous=img
    def _create_window(self):
        # CD-G is 288 pixels across and 192 pixels high
        img = np.ones((192,288,3), np.uint8)
        self.previous = img
        cv2.namedWindow(WINDOW_NAME,flags=cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(WINDOW_NAME,900,600)
        cv2.imshow(WINDOW_NAME, img)
    def render(self,bytestream):
        # every 24 bytes
        jump=24
        pos=0
        while pos<=len(bytestream)-jump:
            block=bytestream[pos:pos+jump]
            if block[0]==packet.PACKET_BEGIN:
                p = packet.Packet(block)
                data = p.decode()
                if data:
                    print(p.name, data)
            pos+=jump


def get(file):
    with open(file,'rb') as f:
        lines = f.read()
    return lines

window = Window(WINDOW_NAME)

img = np.ones((192,288,3), np.uint8)
img[10][10] = (255,255,255)
window.update(img)
lines = get('tester.cdg')
window.render(lines[:10000])

window.update(img)
        

window.wait()
