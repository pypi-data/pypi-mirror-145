
from . import Cache
from . import Convert
import cv2

def Up (poster = None, width = 200, height = 200):

    if poster is None:
        poster = Cache.get_last_img()

    poster = cv2.resize(poster, (width,height)) 
    Cache.set_last_img(poster)    