import cv2
import numpy as np
from bitstring import BitArray

WINDOW_NAME = 'CD+G'

class Window:
    def __init__(self,name):
        self.name = name
        # CD-G is 288 pixels across and 192 pixels high
        img = np.ones((192,288,3), np.uint8)
        self.previous = img
        cv2.namedWindow(WINDOW_NAME,flags=cv2.WINDOW_GUI_NORMAL)
        # Create nicely sized screen with 3:2 aspect ratio
        cv2.resizeWindow(WINDOW_NAME,900,600)
        # Create empty window
        cv2.imshow(WINDOW_NAME, img)
    def resize(self,width,height):
        cv2.resizeWindow(WINDOW_NAME,width,height)
    def wait(self):
        cv2.waitKey(0)
    def update(self,img):
        cv2.imshow(WINDOW_NAME, img)
        self.previous=img
    def render(self,bytestream):
        table={
            1:'Memory Preset',
            6:'Tile Block',
            30:'Load Color Table (upper)',
            31:'Load Color Table (lower)',
            38:'Tile Block (XOR)'
        }
        # every 16 bytes, print
        pos=0
        # for y in range(192): # height
        #     for x in range(288): # width
        while pos<=len(lines)-48:
            block=lines[pos:pos+48]
            cmd = table.get(block[1])
            if cmd:
                print(cmd)
            pos+=48


def get(file):
    with open(file,'rb') as f:
        lines = f.read()
    return lines

window = Window(WINDOW_NAME)

img = np.ones((192,288,3), np.uint8)
img[10][10] = (255,255,255)
window.update(img)
lines = get('test.cdg')
test = lines[20000:]
window.render(lines)
# pos=0
# for y in range(192): # height
#     for x in range(288): # width
#         img[y][x]=(lines[pos],lines[pos],lines[pos])
#         pos+=1

window.update(img)
        

window.wait()
