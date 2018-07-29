from PIL import Image, ImageDraw, ImageFont
from gauge import Gauge

class SteeringAngle(Gauge):
    def __init__(self, fontfile='Roboto-Regular.ttf', size=256):
        self.size = size
        self.fontfile = fontfile
        self.fontbig = ImageFont.truetype(self.fontfile, size=int(self.size/6))
        self.fontsmall = ImageFont.truetype(self.fontfile, size=int(self.size/12))

    def draw_meter(self, angle=0):
        im = Image.new('RGBA', (self.size, self.size), color=Gauge._transparent)

        linewidth=int(self.size*0.018)

        r1=int(self.size/2 * 0.90)
        r2=int(self.size/2 * 0.60)
        r3=r2-linewidth

        center = int(self.size/2)

        draw = ImageDraw.Draw(im)

        maxang = max(270, 270+angle)
        minang = min(270, 270+angle)

        draw.pieslice([center-r1,center-r1,center+r1, center+r1], minang, maxang, Gauge._red)
        draw.pieslice([center-r2+1,center-r2+1,center+r2-1, center+r2-1], minang, maxang, Gauge._transparent)

        draw.line([center, center-r1, center, center-r3], Gauge._gray, width=linewidth)

        draw.chord([center-r2,center-r2,center+r2, center+r2], 180, 360, Gauge._gray)
        draw.chord([center-r3,center-r3,center+r3, center+r3], 180, 360, Gauge._transparent)

        maxtext = self.fontsmall.getsize('Steering Angle')

        angtext = '{0:.0f}'.format(angle)
        draw.text((center - int(maxtext[0]/2), center), 'Steering Angle',
                  fill=Gauge._black, font=self.fontsmall)

        valtext = self.fontbig.getsize(angtext)
        draw.text((center - int(valtext[0]/2), center - int(valtext[1]*1.1)), angtext,
                  fill=Gauge._black, font=self.fontbig)

        return im

if __name__ == '__main__':
    sa = SteeringAngle(size=1024, fontfile='Jura-SemiBold.ttf')
    i = sa.draw_meter(angle=45)

    i.show()
    sa.save_png('sa.png', angle=-45)
