import cv2
import numpy as np
from color import Color
import packet
from time import sleep

WINDOW_NAME = 'CD+G'

class Window:
    def __init__(self,name):
        self.name = name
        # CD-G is 288 pixels across and 192 pixels high
        self.screen = np.zeros((192,288,3), np.uint8)
        self._color_table=[0]*16
        self._ph=0
        self._pv=0
        self._instructions = {
            packet.MEMORY_PRESET:self._mem_preset,
            packet.BORDER_PRESET:self._border_preset,
            packet.TILE_BLOCK:self._tile_block,
            packet.SCROLL_PRESET:self._scroll_preset,
            packet.SCROLL_COPY:self._scroll_copy,
            packet.TRANSPARENT_COLOR:self._def_transparent_color,
            packet.COLOR_TABLE_LOWER:self._load_color_table,
            packet.COLOR_TABLE_UPPER:self._load_color_table,
            packet.TILE_BLOCK_XOR:self._tile_block
        }
        self._create_window()

    def _mem_preset(self,color,repeat):
        self.ph=0
        self.pv=0
        # TODO: Reset everything

    def _border_preset(self,color):
        # TODO: Actually make the border lol
        pass

    def _tile_block(self,color0,color1,row,col,ch,font,xor):
        rgb0=Color(*self._color_table[color0]).rgb[::-1]
        rgb1=Color(*self._color_table[color1]).rgb[::-1]
        self._paint_block(rgb0,rgb1,row,col,font,xor)

    def _scroll_preset(self,color,coph,ph,copv,pv):
        pass

    def _scroll_copy(self,coph,ph,copv,pv):
        pass

    def _def_transparent_color(self,table):
        # TODO: Complete this once rendering is up and running
        pass

    def _load_color_table(self,table,flag):
        if flag==0:
            self._color_table[:8]=table
        elif flag==1:
            self._color_table[8:]=table

    def resize(self,width,height):
        cv2.resizeWindow(WINDOW_NAME,width,height)

    def wait(self):
        cv2.waitKey(0)

    def _update_window(self):
        cv2.imshow(WINDOW_NAME, self.screen)

    def _create_window(self):
        cv2.namedWindow(WINDOW_NAME,flags=cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(WINDOW_NAME,900,600)
        cv2.imshow(WINDOW_NAME, self.screen)

    def _paint_block(self,color0,color1,row,col,pixels,xor):
        y=col*12
        for line in pixels:
            x=row*6
            for i in range(5,-1,-1):
                on = (line&((2**(i+1))-1))>>i
                # if xor:
                #     screen_color=self.screen[y-12][x-12]
                #     color1=(color1[0]^screen_color[0],color1[1]^screen_color[1],color1[2]^screen_color[2])
                #     color0=(color0[0]^screen_color[0],color0[1]^screen_color[1],color0[2]^screen_color[2])
                self.screen[y-12][x-12]=color1 if on else color0
                x+=1
            y+=1
        self._update_window()

    def render(self,bytestream):
        # every 24 bytes
        jump=24
        pos=0
        while pos<=len(bytestream)-jump:
            block=bytestream[pos:pos+jump]
            if block[0]==packet.PACKET_BEGIN:
                p = packet.Packet(block)
                data = p.decode()
                # print(p.name,data)
                run=self._instructions.get(p.instruction)
                run(*p.decode())
            pos+=jump


def get(file):
    with open(file,'rb') as f:
        lines = f.read()
    return lines

window = Window(WINDOW_NAME)

# img = np.ones((192,288,3), np.uint8)
# img[10][10] = (255,255,255)
lines = get('tester.cdg')
window.render(lines[:60000])
# window._paint_block(2,9,[0, 0, 0, 10, 14, 14, 14, 14, 14, 14, 14, 14])

window.wait()
