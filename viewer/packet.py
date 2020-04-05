# Type Constants
MEMORY_PRESET       = 1
BORDER_PRESET       = 2
TILE_BLOCK          = 6
SCROLL_PRESET       = 20
SCROLL_COPY         = 24
TRANSPARENT_COLOR   = 28
COLOR_TABLE_LOWER   = 30
COLOR_TABLE_UPPER   = 31
TILE_BLOCK_XOR      = 38

PACKET_BEGIN        = 9

class Packet:
    def __init__(self,raw):
        self.raw=raw
        self.instruction=self.raw[1]
        self.name=str()
        self.parity={
            'P':self.raw[2:3],
            'Q':self.raw[20:]
        }
        self.data=self.raw[4:20]

    def decode(self):
        instructions = {
            MEMORY_PRESET:['Memory Preset',self._mem_preset],
            BORDER_PRESET:['Border Preset',self._border_preset],
            TILE_BLOCK:['Tile Block',self._tile_block],
            SCROLL_PRESET:['Scroll Preset',self._scroll_preset],
            SCROLL_COPY:['Scroll Copy',self._scroll_copy],
            TRANSPARENT_COLOR:['Define Transparent Color',self._def_transparent_color],
            COLOR_TABLE_LOWER:['Load Color Table (lower)',self._load_color_table],
            COLOR_TABLE_UPPER:['Load Color Table (upper)',self._load_color_table_upper],
            TILE_BLOCK_XOR:['Tile Block (XOR)',self._tile_block_xor]
        }
        _instruction=instructions.get(self.instruction)
        if _instruction:
            self.name=_instruction[0]
            return _instruction[1]()

    def _format_bytes(self,bytestream):
        return ', '.join([str(x) for x in bytestream])

    def _mem_preset(self):
        # Isolate last 4 bits
        color=self.data[0]&15
        repeat=self.data[1]&15
        return (color,repeat)

    def _border_preset(self):
        color=self.data[0]&15
        return (color,)

    def _tile_block(self,xor=0):
        ch=((self.data[0]&48)>>2)|((self.data[1]&48)>>4)
        color0=self.data[0]&15
        color1=self.data[1]&15
        row=self.data[2]&31
        column=self.data[3]&63
        font=[f'{num:06b}' for num in self.data[4:]]
        return (color0,color1,row,column,ch,font,xor)

    def _scroll_preset(self):
        color=self.data[0]&15
        coph=(self.data[1]&48)>>4
        ph=self.data[1]&3
        copv=(self.data[2]&48)>>4
        pv=self.data[2]&15
        return (color,coph,ph,copv,pv)

    def _scroll_copy(self):
        coph=(self.data[1]&48)>>4
        ph=self.data[1]&3
        copv=(self.data[2]&48)>>4
        pv=self.data[2]&15
        return (coph,ph,copv,pv)

    def _def_transparent_color(self):
        return ([x for x in self.data],)

    def _load_color_table(self,flag=0):
        colors=[(self.data[i],self.data[i+1]) for i in range(0,len(self.data),2)]
        return (colors,flag)

    def _load_color_table_upper(self):
        # Wrapper for UPPER
        return self._load_color_table(flag=1)

    def _tile_block_xor(self):
        # Wrapper for XOR
        return self._tile_block(xor=1)

    def __str__(self):
        return ' '.join([self.name,self._format_bytes(self.raw[2:])])

    def __bytes__(self):
        return self.raw
