from PIL import Image, ImageDraw, ImageFont
import math

class Gauge(object):
    _white = (255,255,255,255)
    _black = (0,0,0,255)
    _gray = (128,128,128,255)
    _gray2 = (64,64,64,255)
    _maxG = 1.25
    _transparent = (255,255,255,0)
    _red = (255,0,0,255)
    _warning = (200,200,0,255)
    _fontcolor = _black

    def __init__(self):
        pass

    def draw_meter(self, **kwargs):
        raise NotImplemented


    def save_png(self, name='default.png', **kwargs):
        im = self.draw_meter(**kwargs)

        im.save(name)
