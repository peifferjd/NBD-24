import streamlit as st
from PIL import Image as pImage
import tempfile
import numpy as np
import os


# key = np.random.choice(Image.fetch('KEY'))
# _, array = (Image & key).fetch1('fname', 'image')
# # save array as tmpfile
# fname = tempfile.mktemp(suffix='.png')
# pImage.fromarray(array).save(fname)
# fname='dwaynejohnson.jpg'

# label_list = ['eye','na']
# result_dict = {'points':[[0,0]],'labels':[1]}

# new_labels=None
# new_labels = pointdet(image_path=fname, 
#                         label_list=label_list, 
#                         points=result_dict['points'],
#                         labels=result_dict['labels'],
#                         key=fname)
# if new_labels is not None:
#     result_dict['points'] = [v['point'] for v in new_labels]
#     result_dict['labels'] = [v['label_id'] for v in new_labels]
#     st.json(result_dict)
#     # cleanup temp
#     print("HI")
#     st.rerun()


# import streamlit as st
# from glob import glob
# from streamlit_image_annotation import pointdet

# label_list = ['eye','na']
# image_path_list = glob('*.jpg')
# if 'result_dict' not in st.session_state:
#     result_dict = {}
#     for img in image_path_list:
#         result_dict[img] = {'points': [[0,0]],'labels':[1]}
#     st.session_state['result_dict'] = result_dict.copy()

# target_image_path = image_path_list[0]

# new_labels = pointdet(image_path=target_image_path, 
#                         label_list=label_list, 
#                         points=st.session_state['result_dict'][target_image_path]['points'],
#                         labels=st.session_state['result_dict'][target_image_path]['labels'], key=target_image_path)
# if new_labels is not None:
#     st.session_state['result_dict'][target_image_path]['points'] = [v['point'] for v in new_labels]
#     st.session_state['result_dict'][target_image_path]['labels'] = [v['label_id'] for v in new_labels]
#st.json(st.session_state['result_dict'])


import streamlit as st
import numpy as np
# from annotation_schema import CroppedImage
from streamlit_image_coordinates import streamlit_image_coordinates
import os

# def get_random_image():
#     key = np.random.choice(CroppedImage.fetch('KEY'))
#     _, array = (CroppedImage & key).fetch1('fname', 'image')
#     random_filename = f'{key["fname"].split(".")[0]}{np.random.randint(0,10000)}.png'

# #     pImage.fromarray(array).save(random_filename)
# #     return random_filename


# # fname = get_random_image()
# array = np.load("kitty.npy")
# st.write(array.shape)

# value = streamlit_image_coordinates(array,key='numpy')

# st.write(value)


if 'points' not in st.session_state:
    st.session_state['points'] = []
    
from PIL import Image, ImageDraw
def get_ellipse_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
    center = point
    radius = 10
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )

array = np.load("kitty.npy")
with Image.fromarray(array) as img:
    draw = ImageDraw.Draw(img)

    # Draw an ellipse at each coordinate in points
    for point in st.session_state["points"]:
        coords = get_ellipse_coords(point)
        draw.ellipse(coords, fill="red")

    value = streamlit_image_coordinates(img, key="pil")

    if value is not None:
        point = value["x"], value["y"]

        if point not in st.session_state["points"]:
            st.session_state["points"].append(point)
            st.experimental_rerun()