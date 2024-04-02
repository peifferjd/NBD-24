from glob import glob
from PIL import Image as pImage
import datajoint as dj
dj.config['database.host']= '137.184.112.232'
from annotation_schema import Image,Label
import numpy as np
import matplotlib.pyplot as plt

image_list = glob('faces_unannotated/*')
current_keys = Image.fetch('fname')

def load_image(path):
    # Load the image
    img = pImage.open(path)

    # Resize the image
    img_resized = img.resize((384, 286), pImage.Resampling.LANCZOS)

    # Convert the image to a NumPy array
    img_array = np.array(img_resized)[:,:,:3]
    assert img_array.shape == (286, 384, 3)
    fname = path.split('/')[-1]
    return {'image': img_array, 'fname': fname}

for path in image_list:
    if path.split('/')[-1] not in current_keys:
        Image.insert1(load_image(path))
        print('inserted', path)