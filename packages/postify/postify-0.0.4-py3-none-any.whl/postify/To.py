import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from . import Cache

def local_file (path, poster = None):

    if poster is None:
        poster = Cache.get_last_img()

    # Save as output
    _ = np.uint8(poster)
    img = Image.fromarray(_, 'RGB')
    img.save(path)

def notebook ( poster = None, size = 5):

    if poster is None:
        poster = Cache.get_last_img()

    # Show in NOTEBOOK if needed
    plt.figure(figsize=(size, size), dpi=80)
    plt.imshow(poster/255, interpolation='nearest')
    plt.show()

def stats ( poster = None ):

    if poster is None:
        poster = Cache.get_last_img()

    print("Poster shape:", poster.shape)
    print(f"Ratio: {poster.shape[1]/poster.shape[0]}")