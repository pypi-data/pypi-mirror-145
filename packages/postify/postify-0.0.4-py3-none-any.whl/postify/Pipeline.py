import os, glob
from . import Cache
from . import To, From
_pipeline = []
_names = []
from IPython.display import clear_output


def _set_pipeline ( items ):
    global _pipeline
    _pipeline = items

def _get_pipeline ():
    global _pipeline
    return _pipeline

def InputFiles ( match ):
    files = glob.glob(match)
    InputFileList(files)

def InputFileList ( files ):
    images = []
    for file in files:
        print("Loading: " + file, end = '\r')
        From.local_file(file)
        images.append(Cache.get_last_img())
    _set_pipeline(images)
    global _names
    _names = files
    print(f"Loaded {len(files)} images", " " * 200)


def RunWith ( callback):
    results = []
    global _names
    for i,file in enumerate(_get_pipeline()):
        print("Running: " + _names[i], end='\r')
        Cache.set_last_img(file)
        callback(_names[i])
        results.append(Cache.get_last_img())
    _set_pipeline(results)
    print(f"Ran {len(_get_pipeline())} images", " " * 200)

def SaveFiles (directory):
    global _names
    for i, img in enumerate(_get_pipeline()):
        filename = os.path.basename(_names[i])
        filename = os.path.join(directory, filename)
        Cache.set_last_img(img)
        print("Saving: " + filename, end='\r')
        To.local_file(filename)
    print(f"Saved {len(_get_pipeline())} images", " " * 200)

    
def Show ( number = 3):
    print("Showing: " + str(number) + " images of " + str(len(_get_pipeline())))
    if number > len(_get_pipeline()):
        number = len(_get_pipeline())
    for i in range(number):
        Cache.set_last_img(_get_pipeline()[i])
        To.notebook()

def RunSequential ( match_path, output_path, callback ):
    files = glob.glob(match_path)
    RunSequentialFiles(files, output_path, callback)

def RunSequentialFiles ( files, output_path, callback ):
    for i,f in enumerate(files):
        print(f"Running: {i} / {len(files)}")
        InputFileList([f])
        RunWith(callback)
        SaveFiles(output_path)
        clear_output()    

