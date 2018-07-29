from PIL import Image, ImageDraw, ImageFont
import math
from gauge import Gauge

class RPM(Gauge):
    def __init__(self, fontfile='Roboto-Regular.ttf', size=256):
        self.size = size
        self.fontfile = fontfile
        self.fontbig = ImageFont.truetype(self.fontfile, size=int(self.size/4))
        self.fontsmall = ImageFont.truetype(self.fontfile, size=int(self.size/6))
        self.maxrpm = 0

    def _maxrpm(self, rpm):
        self.maxrpm = max(self.maxrpm, rpm)

    def _rangerpm(self, rpm):
        rpmang = 135 + int((rpm/8000)*270)

        return rpmang

    def draw_meter(self, rpm):
        self._maxrpm(rpm)
        im = Image.new('RGBA', (self.size, self.size), color=Gauge._transparent)

        linewidth = int(self.size*0.018)

        r1 = int(self.size/2 * 0.95)
        r2 = int(self.size/2 * 0.75)
        r3 = r2-linewidth
        r4 = int(self.size / 2 * 0.90)

        center = int(self.size/2)

        draw = ImageDraw.Draw(im)

        rpmang = self._rangerpm(rpm)
        rpmmax = self._rangerpm(self.maxrpm)

        draw.pieslice([center-r1,center-r1,center+r1, center+r1], 405-int(1.5*33.75), 405, Gauge._warning)
        draw.pieslice([center-r2+1,center-r2+1,center+r2-1, center+r2-1], 405-int(1.5*33.75), 405, Gauge._transparent)

        draw.pieslice([center-r4,center-r4,center+r4, center+r4], 135, rpmang, Gauge._red)
        draw.pieslice([center-r2+1,center-r2+1,center+r2-1, center+r2-1], 135, rpmang, Gauge._transparent)

        x = math.cos(math.radians(rpmmax))
        y = math.sin(math.radians(rpmmax))
        draw.line([int(x*(r1))+center, int(y*(r1))+center, int(x*r2)+center, int(y*r2)+center],
                      Gauge._red, width=2)

        for marker in range(0, 9):
            ang = 135 + (marker*33.75)
            x = math.cos(math.radians(ang))
            y = math.sin(math.radians(ang))
            draw.line([int(x*(r1+10))+center, int(y*(r1+10))+center, int(x*r2)+center, int(y*r2)+center],
                      Gauge._gray2, width=int(linewidth/2))

        draw.chord([center-r2, center-r2, center+r2, center+r2],  135, 405, Gauge._gray)
        draw.chord([center-r3, center-r3, center+r3, center+r3],  115, 425, Gauge._transparent)
        draw.arc([center-r4, center-r4, center+r4, center+r4],  135, 405, Gauge._gray2)


        maxtext = self.fontsmall.getsize('RPM')

        rpmtext = '{0:.0f}'.format(rpm)

        draw.text((center - int(maxtext[0]/2), int(center*1.4)), 'RPM', fill=Gauge._black, font=self.fontsmall)

        valtext = self.fontbig.getsize(rpmtext)

        draw.text((center - int(valtext[0]/2), int(center*1.2) - int(valtext[1]*1.1)),
                  rpmtext, fill=Gauge._black, font=self.fontbig)


        return im

if __name__ == '__main__':
    sa = RPM(size=350, fontfile='Roboto-Medium.ttf')
    i = sa.draw_meter(rpm=4200)

    i = sa.draw_meter(rpm=2000)

    sa.save_png(name='test.png', rpm=999)
    i.show()
