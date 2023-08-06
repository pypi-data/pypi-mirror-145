import math
import numpy as np
from . import Cache

def Square (poster = None, pad = False, color = (0, 0, 255)):
    if poster is None:
        poster = Cache.get_last_img()
        
    # Get the dimensions of the image
    height, width, _ = poster.shape

    if (height == width):
        return

    if height > width:
        if pad :
            new_poster = np.zeros((height,height,3), np.uint8)
            new_poster[:,:] = color
            half = math.floor((height - width)/2)
            new_poster[:,half:half+width] = poster
            Cache.set_last_img(new_poster)
        else:
            new_poster = np.zeros((width,width,3), np.uint8)
            new_poster[:,:] = color
            half = math.floor((height - width)/2)
            new_poster[:,:] = poster[half:half+width,:]
            Cache.set_last_img(new_poster)
            
    else:
        poster = np.moveaxis(poster, 0, 1)
        Cache.set_last_img(poster)
        Square(poster=poster, pad=pad, color=color)
        poster = Cache.get_last_img()
        poster = np.moveaxis(poster, 1, 0)
        Cache.set_last_img(poster)

def Smart (poster = None, tolerance = 0.40, margin = 0.05) :

    tolerance *= 255

    if poster is None:
        poster = Cache.get_last_img()

    margin = math.floor(margin *poster.shape[0]) + 1

    def do_side () :
        def try_value (value) :
            pixels = math.floor(value * poster.shape[0])
            area = poster[0:pixels,:]
            return np.max(area) < tolerance
        step = 0.5
        pos = 0
        tries = 0
        while tries < 400:
            tries += 1
            if try_value(pos + step):
                pos += step
            else:
                step /= 2
                if step < 0.003:
                    break
        return pos
    

    y = do_side()
    poster = np.moveaxis(poster, 0, 1)
    x = do_side()
    poster = np.moveaxis(poster, 0, 1)
    poster = np.flip(poster, 0)
    poster = np.flip(poster, 1)
    _y = do_side()
    poster = np.moveaxis(poster, 0, 1)
    _x = do_side()
    poster = np.moveaxis(poster, 0, 1)
    poster = np.flip(poster, 0)
    poster = np.flip(poster, 1)

    y = math.floor(y * poster.shape[0])
    x = math.floor(x * poster.shape[1])
    _y = math.floor(_y * poster.shape[0])
    _x = math.floor(_x * poster.shape[1])

    if (_y < margin):
        _y = margin
    if (_x < margin):
        _x = margin
    if (y < margin):
        y = margin
    if (x < margin):
        x = margin

    height = poster.shape[0] - y - _y + margin * 2
    width = poster.shape[1] - x - _x + margin * 2
    new_poster = np.zeros((height, width, 3), np.uint8)

    new_poster[:,:] = poster[
        y-margin    :   poster.shape[0]-_y+margin,
        x-margin    :   poster.shape[1]-_x+margin]

    Cache.set_last_img(new_poster)


def Edges (poster = None, ratio = 1):
    if poster is None:
        poster = Cache.get_last_img()
        
    # Get the dimensions of the image
    height, width, _ = poster.shape

    target_width = math.floor(width * ratio)
    half_border = math.floor((width-target_width) / 2)

    # Create a new image with the same dimensions as the original
    new_poster = np.zeros((height, target_width, 3), np.uint8)
    new_poster[:,:] = (0, 0, 0)

    # Copy the original image into the new image
    new_poster[:,:] = poster[:,half_border:half_border+target_width]

    # Save
    Cache.set_last_img(new_poster)