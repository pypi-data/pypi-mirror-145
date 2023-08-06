import importlib, postify, cv2, math, os
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from . import Cache
from . import Convert

Fonts = {
    "Jura" : "/Users/eric/Documents/Projects/poster-designer/postify/fonts/Jura-Medium.ttf",
}

def _with_text ( poster = None, font="", text="", x=0, y=0, size=0.1, x_off = 1, y_off = 1, color=(0,255,0)):
    
    # Get poster
    if poster is None:
        poster = Cache.get_last_img()

    # Get pixels
    x, y = Convert.to_pixels(width = x, height = y)

    layer = np.zeros(poster.shape, dtype=np.uint8) + 1
    image = Image.fromarray(layer)    
    draw = ImageDraw.Draw(image)

    size, _ = Convert.to_pixels(width = size, height=size)
    
    # load font
    font = ImageFont.truetype(font, size)  

    w, h = draw.textsize(text, font=font)
    x = x - (x_off * w//2)
    y = y - (y_off * h//2)

    # positioning
    draw.text((x,y,0),text,(math.floor(color[0]*255),math.floor(color[1]*255),math.floor(color[2]*255)),font=font)
    
    i = np.array(image)
    poster[i!=1] = i[i!=1]

def Center ( poster = None, font="", text="", x=0.5, y=0.5, size=0.1, color=(0,255,0)):
    _with_text(poster=poster, font=font, text=text, x=x, y=y, size=size, color=color)

def LeftAlign ( poster = None, font="", text="", x=0, y=0.5, size=0.1, color=(0,255,0)):
    _with_text(poster=poster, font=font, text=text, x=x, y=y, size=size, color=color, x_off=0)

def RightAlign ( poster = None, font="", text="", x=0, y=0.5, size=0.1, color=(0,255,0)):
    _with_text(poster=poster, font=font, text=text, x=x, y=y, size=size, color=color, x_off=2)