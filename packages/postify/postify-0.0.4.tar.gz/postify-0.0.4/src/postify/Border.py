import numpy as np
import cv2
from . import Cache
from . import Convert
from . import To
from . import Effects

def _with_borders ( poster = None, left = 0, right = 0, top = 0, bottom = 0, color = (0,255,0), resize = True):
    
    # Get pixels
    left, top = Convert.to_pixels(width = left, height = top)
    right, bottom = Convert.to_pixels(width = right, height = bottom)

    # Get poster
    if poster is None:
        poster = Cache.get_last_img()

    # Change size
    if (resize):

        new_poster = np.zeros((poster.shape[0]+top+bottom, poster.shape[1]+left+right, 3))
        new_poster[:,:] = color
        new_poster[top:top+poster.shape[0], left:left+poster.shape[1]] = poster

        # Save
        Cache.set_last_img(new_poster)

    # Draw borders
    else:
        if top:
            poster[:top,:] = color
        if bottom:
            poster[-bottom:,:] = color
        if left:
            poster[:,:left] = color
        if right:
            poster[:,-right:] = color


def Even ( poster = None, size = 0, color = (0,255,0), resize = False):

    # Get pixels for even borders
    pix_x, pix_y = Convert.to_pixels(width = size, height=size)
    percent_x, percent_y = Convert.to_percent(width = pix_x, height = pix_x)

    _with_borders(poster=poster, left=size, right=size, top=percent_y, bottom=percent_y, color=color, resize=resize)

def Full ( poster = None, size = 0, color = (0,255,0), resize = False):
    _with_borders(poster=poster, left=size, right=size, top=size, bottom=size, color=color, resize=resize)
    
def Chin ( poster = None, size = 0, color = (0,255,0), resize = False):
    _with_borders(poster=poster, bottom=size, color=color, resize=resize)

def Head ( poster = None, size = 0, color = (0,255,0), resize = False):
    _with_borders(poster=poster, top=size, color=color, resize=resize)

def Sides ( poster = None, size = 0, color = (0,255,0), resize = False):
    _with_borders(poster=poster, left=size, right=size, color=color, resize=resize)

def Rounded( poster = None, radius = 0.1, color = (0,255,0)):

    radius, _ = Convert.to_pixels(width = radius, height=radius)
    c = color

    if poster is None:
        poster = Cache.get_last_img()

    t = 2

    h, w = poster.shape[:2]

    # Create new image (three-channel hardcoded here...)
    new_image = np.zeros((h, w, 3), np.uint8)

    # Draw four rounded corners
    new_image = cv2.ellipse(new_image, (int(radius-t/2), int(radius-t/2)), (radius, radius), 180, 0, 90, c, t)
    new_image = cv2.ellipse(new_image, (int(w-radius+4*t/2-1), int(radius-t/2)), (radius, radius), 270, 0, 90, c, t)
    new_image = cv2.ellipse(new_image, (int(radius-t/2), int(h-radius+4*t/2-1)), (radius, radius), 90, 0, 90, c, t)
    new_image = cv2.ellipse(new_image, (int(w-radius+4*t/2-1), int(h-radius+4*t/2-1)), (radius, radius), 0, 0, 90, c, t)

    cv2.floodFill(new_image, None, (0,0), c)
    cv2.floodFill(new_image, None, (w-1,0), c)
    cv2.floodFill(new_image, None, (0,h-1), c)
    cv2.floodFill(new_image, None, (w-1,h-1), c)

    r = new_image[:,:,0]==c[0]
    g = new_image[:,:,1]==c[1]
    b = new_image[:,:,2]==c[2]

    _all = r & g & b

    poster[_all] = new_image[_all]
    

def Blurred( poster = None, size = 0.1, intensity = 0.1):

    if poster is None:
        poster = Cache.get_last_img()
    original_img = np.copy(poster)
    
    Even(size=size, color = (123,123,123))
    bordered = Cache.get_last_img()

    Cache.set_last_img(original_img)
    Effects.blur(size=intensity)
    blur = Cache.get_last_img()

    where = bordered[:,:,0]==123
    original_img[where] = blur[where]

    Cache.set_last_img(original_img)