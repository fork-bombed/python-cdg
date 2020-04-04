class Color:
    def __init__(self,high,low):
        self.high=high
        self.low=low
        self.color=self._convert()
        self.rgb=self._to_rgb()
    def _convert(self):
        red = (self.high&63)>>2
        green = ((self.high&3)<<2)|((self.low>>4)&3)
        blue = self.low&15
        return (red,green,blue)
    def _to_rgb(self):
        rgb = [int((color/15)*255) for color in self.color]
        return tuple(rgb)