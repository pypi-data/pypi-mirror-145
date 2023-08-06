import cv2
import numpy as np
from . import Cache, Convert

def blur (poster = None, size = 0.02):

    # Get poster
    if poster is None:
        poster = Cache.get_last_img()
    
    # Get pixels for even borders
    size, _ = Convert.to_pixels(width=size, height=size)

    Cache.set_last_img(cv2.blur(poster, (size,size)))

def denoise (poster = None):

    if poster is None:
        poster = Cache.get_last_img()

    Cache.set_last_img(
        cv2.fastNlMeansDenoisingColored(poster,None,10,10,7,21)   
    )

def brighter (poster = None, amount = 50):

    if poster is None:
        poster = Cache.get_last_img()

    poster = poster.astype(np.float32)

    adjusted = cv2.convertScaleAbs(poster, alpha=1.5, beta=amount)
    adjusted = adjusted - adjusted.min()
    adjusted = adjusted * (255 / adjusted.max())
    Cache.set_last_img(adjusted)

def contrasty (poster = None, amount = 1.5) :

    if poster is None:
        poster = Cache.get_last_img()

    adjusted = cv2.convertScaleAbs(poster, alpha=amount, beta=0)
    Cache.set_last_img(adjusted)

def drop (poster = None, cuttoff = 0.5):

    if poster is None:
        poster = Cache.get_last_img()

    total = np.sum(poster, axis=(0,1))
    std = np.std(poster)
    mean = np.mean(poster)

    cutoff = mean - (std * cuttoff)

    poster -= cuttoff
    poster[poster < 0] = 0
    poster *= 255/poster.max()

def normalize (poster = None ):
    if poster is None:
        poster = Cache.get_last_img()

    poster -= poster.min()
    poster *= 255/poster.max()
    
    Cache.set_last_img(poster)


def ApplyGradient (poster = None, white_to = (255,0,0), black_to = (0,0,255)) :
    if poster is None:
        poster = Cache.get_last_img()

    poster = (poster/255) * white_to + (1 - (poster/255)) * black_to
    Cache.set_last_img(poster)

def Invert (poster = None):
    if poster is None:
        poster = Cache.get_last_img()
    poster = poster.astype(np.float32)
    poster = poster * -1 + 255
    Cache.set_last_img(poster)

def ReplaceColor (poster = None, color = (255,0,0), replace = (0,0,0)):
    if poster is None:
        poster = Cache.get_last_img()
    poster = poster.astype(np.float32)
    poster[poster == color] = replace
    Cache.set_last_img(poster)