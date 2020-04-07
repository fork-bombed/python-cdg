import cv2
import numpy as np
from color import Color
import packet

WINDOW_NAME = 'CD+G'

class Window:
    def __init__(self,name):
        self.name = name
        # CD-G is 288 pixels across and 192 pixels high
        self.screen = np.zeros((216,300,3), np.uint8)
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
        self._empty_screen()
        # TODO: Reset everything

    def _border_preset(self,color):
        # TODO: Actually make the border lol
        pass

    def _tile_block(self,color0,color1,row,col,ch,font,xor):
        bgr0=Color(*self._color_table[color0]).bgr
        bgr1=Color(*self._color_table[color1]).bgr
        self._paint_block(bgr0,bgr1,row,col,font,xor)
        self._update_window()

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
        # TODO: Asyncronous updates
        cv2.imshow(WINDOW_NAME, self.screen)

    def _empty_screen(self):
        self.screen = np.zeros((216,300,3), np.uint8)
        self._update_window()

    def _create_window(self):
        cv2.namedWindow(WINDOW_NAME,flags=cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(WINDOW_NAME,900,648)
        self._empty_screen()

    def _paint_block(self,color0,color1,row,col,pixels,xor):
        y=(col-1)*12
        x=(row-1)*6
        border_x=6
        border_y=12
        offset_y=0
        for line in pixels:
            offset_x=0
            for i in range(5,-1,-1):
                on = (line&((2**(i+1))-1))>>i
                if xor:
                    color=color1 if on else color0
                    color=tuple([color[i]^self.screen[sum([border_y,offset_y,y])][sum([border_x,offset_x,x])][i] for i in range(3)])
                    self.screen[sum([border_y,offset_y,y])][sum([border_x,offset_x,x])]=color
                else:
                    self.screen[sum([border_y,offset_y,y])][sum([border_x,offset_x,x])]=color1 if on else color0
                offset_x+=1
            offset_y+=1

    def render(self,bytestream):
        # every 24 bytes
        jump=24
        pos=0
        while pos<=len(bytestream)-jump:
            block=bytestream[pos:pos+jump]
            if block[0]==packet.PACKET_BEGIN:
                p = packet.Packet(block)
                run=self._instructions.get(p.instruction)
                run(*p.decode())
            pos+=jump


def get(file):
    with open(file,'rb') as f:
        lines = f.read()
    return lines

window = Window(WINDOW_NAME)

lines = get('test.cdg')
window.render(lines[:65500])

window.wait()
