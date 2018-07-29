from PIL import Image, ImageDraw, ImageFont
from gauge import Gauge

class Speedometer(Gauge):
    def __init__(self, fontfile='Roboto-Regular.ttf', size=256, units='mph'):
        self.size = size
        self.fontfile = fontfile
        self.fontbig = ImageFont.truetype(self.fontfile, size=int(self.size/2 * 0.8 ))
        self.fontsmall = ImageFont.truetype(self.fontfile, size=int(self.size/2 * 0.2 ))
        self.units = units

    def _convert_units(self, speed):
        if self.units == 'kph':
            return speed
        elif self.units == 'mph':
            return int(speed * 0.621371)

        raise TypeError

    def draw_meter(self, speed):
        speed = self._convert_units(speed)

        im = Image.new('RGBA', (self.size, int(self.size/2)), color=self._transparent)
        draw = ImageDraw.Draw(im)

        draw.text((0,0), '{0:.0f}'.format(speed),
                  fill=Gauge._fontcolor, font=self.fontbig)

        draw.text((int(self.size*.75), int(self.size/2 * 0.57)), self.units,
                  fill=Gauge._fontcolor, font=self.fontsmall)

        return im

if __name__ == '__main__':
    speed = Speedometer(size=256, fontfile='Jura-SemiBold.ttf', units='kph')
    i = speed.draw_meter(speed=40)
    i.show()





