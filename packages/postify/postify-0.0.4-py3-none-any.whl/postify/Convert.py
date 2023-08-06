import math
from . import Cache

def to_pixels ( poster = None, width = 0, height = 0 ):

    if poster is None:
        poster = Cache.get_last_img()

    height = math.floor(height * poster.shape[0])
    width = math.floor(width * poster.shape[1])

    return (width, height)

def to_percent ( poster = None, width = 0, height = 0 ):

    if poster is None:
        poster = Cache.get_last_img()

    height = height / poster.shape[0]
    width = width / poster.shape[1]

    return (width, height)