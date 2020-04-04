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

class Packet:
    def __init__(self,data):
        self.data=data
        self.instruction=0
        self.name=str()
        self._run_instruction()
    def _run_instruction(self):
        instructions = {
            MEMORY_PRESET:['Memory Preset',self._mem_preset],
            BORDER_PRESET:['Border Preset',self._border_preset],
            TILE_BLOCK:['Tile Block',self._tile_block],
            SCROLL_PRESET:['Scroll Preset',self._scroll_present],
            SCROLL_COPY:['Scroll Copy',self._scroll_copy],
            TRANSPARENT_COLOR:['Define Transparent Color',self._def_transparent_color],
            COLOR_TABLE_LOWER:['Load Color Table (lower)',self._load_color_table_lower],
            COLOR_TABLE_UPPER:['Load Color Table (upper)',self._load_color_table_upper],
            TILE_BLOCK_XOR:['Tile Block (XOR)',self._tile_block_xor]
        }
        raw_instruction = self.data[1]
        instruction = instructions.get(raw_instruction)
        self.instruction=raw_instruction
        self.name=instruction[0]
        instruction[1]()
    def _mem_preset(self):
        pass
    def _border_preset(self):
        pass
    def _tile_block(self,xor=0):
        pass
    def _scroll_present(self):
        pass
    def _scroll_copy(self):
        pass
    def _def_transparent_color(self):
        pass
    def _load_color_table_lower(self):
        pass
    def _load_color_table_upper(self):
        pass
    def _tile_block_xor(self):
        # Wrapper for XOR
        self._tile_block(xor=1)
    def __str__(self):
        return ' '.join([self.name,', '.join([str(x) for x in self.data[2:]])])
