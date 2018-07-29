from PIL import Image, ImageDraw, ImageFont
from gauge import Gauge

class GMeter(Gauge):
    def __init__(self, fontfile='Jura-SemiBold.ttf', size=256):
        self.size = size
        self.fontfile = fontfile
        self.fontbig = ImageFont.truetype(self.fontfile, size=int(self.size/10))
        self.fontsmall = ImageFont.truetype(self.fontfile, size=int(self.size/15))
        self.min_max_x = [0,0]
        self.min_max_y = [0,0]

    def setminmax(self, x, y):
        if x < self.min_max_x[0]:
            self.min_max_x[0] = x
        if x > self.min_max_x[1]:
            self.min_max_x[1] = x
        if y < self.min_max_y[0]:
            self.min_max_y[0] = y
        if y > self.min_max_y[1]:
            self.min_max_y[1] = y

    def scalexy(self, x,y, r1):
        xscale = int(( x / self._maxG ) * r1)
        yscale = int(( y / self._maxG ) * r1)


        return xscale, yscale

    def draw_meter(self, x, y):
        im = Image.new('RGBA', (self.size, self.size), color=self._transparent)

        r1=int(self.size/2 * 0.61)
        r2=int(self.size/2 * 0.59)
        r3=int(self.size * 0.0234)
        r4=int(r3 * 1.8)

        self.setminmax(x,y)
        xscale, yscale = self.scalexy(x,y,r1)

        center = int(self.size/2)

        draw = ImageDraw.Draw(im)

        draw.ellipse([center-r1,center-r1,center+r1, center+r1], Gauge._gray)
        draw.ellipse([center-r2,center-r2,center+r2, center+r2], Gauge._black)
        draw.line([center-r2, center, center+r2, center], (64,64,64,255), width=2)
        draw.line([center, center-r2, center, center+r2], (64,64,64,255), width=2)

        maxtext = self.fontbig.getsize(str(self._maxG))

        draw.text((0, int(center - maxtext[1]/2) - 2), str(self._maxG), 
		          fill=Gauge._fontcolor, font=self.fontbig)
        draw.text((self.size - maxtext[0] -2, int(center - maxtext[1]/2) - 2), str(self._maxG), 
		          fill=Gauge._fontcolor, font=self.fontbig)
        draw.text((center-int(maxtext[0]/2), (center-r1-maxtext[1]-6)), str(self._maxG), fill=Gauge._fontcolor, font=self.fontbig)
        draw.text((center-int(maxtext[0]/2), (center+r1)), str(self._maxG), fill=Gauge._fontcolor, font=self.fontbig)

        textmin = self.fontsmall.getsize("Xmax: -0.00")

        draw.text((2, 2), 'X: {0:.2f}'.format(x), fill=Gauge._fontcolor, font=self.fontsmall)
        draw.text((2, 2+(textmin[1])), 'Y: {0:.2f}'.format(y), fill=Gauge._fontcolor, font=self.fontsmall)


        draw.text((2, self.size-2-(textmin[1])), 'Xmin: {0:.2f}'.format(self.min_max_x[0]), 
                    fill=Gauge._fontcolor, font=self.fontsmall)
        draw.text((2, self.size-2-(2*textmin[1])), 'Xmax: {0:.2f}'.format(self.min_max_x[1]), 
                    fill=Gauge._fontcolor, font=self.fontsmall)

        draw.text((self.size - 2 - textmin[0], self.size-2-(textmin[1])),
                  'Ymax: {0:.2f}'.format(self.min_max_y[1]), fill=Gauge._fontcolor, font=self.fontsmall)
        draw.text((self.size - 2 - textmin[0], self.size-2-(2*textmin[1])),
                  'Ymin: {0:.2f}'.format(self.min_max_y[0]), fill=Gauge._fontcolor, font=self.fontsmall)

        centerx = center + xscale
        centery = center - yscale

        draw.ellipse([centerx-r4, centery-r4, centerx+r4, centery+r4], Gauge._transparent, self._white)
        draw.line([centerx - r4 - 5, centery, centerx+r4+5, centery ], Gauge._white, width=2)
        draw.line([centerx, centery - r4 -5, centerx, centery + r4 + 5], Gauge._white, width=2)
        draw.ellipse([centerx-r3, centery-r3, centerx+r3, centery+r3], Gauge._red)

        return im

if __name__ == '__main__':
    gmeter = GMeter(size=1024, fontfile='Jura-SemiBold.ttf')
    i = gmeter.draw_meter(x=0.25, y=-0.25)
    i.show()
    gmeter.save_png(name='test_gmeter.png', x=0.625, y=0)

