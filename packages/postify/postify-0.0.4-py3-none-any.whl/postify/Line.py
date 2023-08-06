import importlib, postify, cv2, math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import pathlib
from . import Cache
from . import Convert

def _with_line ( poster = None, x = 0, y = 0, x2 = 0, y2 = 0, thickness=4, color=(0,0,0)):
    
    # Get pixels
    x, y = Convert.to_pixels(width = x, height = y)
    x2, y2 = Convert.to_pixels(width = x2, height = y2)
    thickness, _ = Convert.to_pixels(width = thickness, height = thickness)
    
    # Get poster
    if poster is None:
        poster = Cache.get_last_img()

    # Draw line
    cv2.line(poster, (x,y), (x2,y2), color, thickness)

def Horizontal ( poster = None, height=0.5, thickness=0.01, color=(0,0,0)):
    
    # Get poster
    if poster is None:
        poster = Cache.get_last_img()

    w,h,_ = poster.shape
    _with_line(poster=poster, x = 0, x2 = w, y=height, y2=height, thickness=thickness, color=color)

def Vertical ( poster = None, depth=0.5, thickness=0.01, color=(0,0,0)):
    
    # Get poster
    if poster is None:
        poster = Cache.get_last_img()

    w,h,_ = poster.shape
    _with_line(poster=poster, y = 0, y2 = h, x=depth, x2=depth, thickness=thickness, color=color)

