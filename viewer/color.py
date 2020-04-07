class Color:
    def __init__(self,high,low):
        self.high=high
        self.low=low
        self.color=self._convert()
        self.bgr=self._to_bgr()
    def _convert(self):
        # Isolate lower 4 bits of high
        red = (self.high&63)>>2
        # Combine lower 2 bits of high (MSB) and lower 2 bits of low (LSB)
        green = ((self.high&3)<<2)|(((self.low&63)>>4)&3)
        # Isolate lower 4 bits of low
        blue = self.low&15
        return (red,green,blue)
    def _to_bgr(self):
        # Find percentage and use to get value out of 255
        bgr = [int((color/15)*255) for color in self.color][::-1]
        return tuple(bgr)