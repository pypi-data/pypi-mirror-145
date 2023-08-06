import cv2, math
import numpy as np
from . import Cache

def local_file ( path ):
    _ = cv2.imread(path)
    _ = cv2.cvtColor(_, cv2.COLOR_BGR2RGB)
    Cache.set_last_img(_)
    return _

def blank ( width = 100, height = 0, ratio = 0.75, color=(255,0,0) ):
    
    # Load via width and ratio
    if ratio > 0:
        height = math.floor(width * (1/ratio))
    
    # Load via width and height
    if width > 0 and height > 0:
        img = np.zeros((height,width,3), np.uint8)
        img[:,:] = color
        Cache.set_last_img(img)
        return img
    
    raise Exception("Must provide either a (width, height) or a (width, ratio) to form blank image")
