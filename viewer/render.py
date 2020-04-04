import cv2
import numpy as np
from bitstring import BitArray
from color import Color
from packet import *

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
        # every 24 bytes, print
        jump=24
        pos=0
        while pos<=len(bytestream)-jump:
            block=bytestream[pos:pos+jump]
            if block[0]==9:
                packet = Packet(block)
                # if cmd and (cmd==table[30] or cmd==table[31]):
                if packet.instruction == COLOR_TABLE_LOWER or packet.instruction == COLOR_TABLE_UPPER:
                    print(packet)
                    # data = block.hex()
                    # print(' '.join([data[i:i+2].upper() for i in range(0, len(data), 2)]))
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
window.render(lines[:100000])
# pos=0
# for y in range(192): # height
#     for x in range(288): # width
#         img[y][x]=(lines[pos],lines[pos],lines[pos])
#         pos+=1

window.update(img)
        

window.wait()
