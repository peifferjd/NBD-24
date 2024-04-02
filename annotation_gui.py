# import streamlit as st
# from streamlit_image_annotation import pointdet
# # from annotation_schema import Image, Label
# from PIL import Image as pImage
# import tempfile
# import numpy as np
# import os


# # key = np.random.choice(Image.fetch('KEY'))
# # _, array = (Image & key).fetch1('fname', 'image')
# # # save array as tmpfile
# # fname = tempfile.mktemp(suffix='.png')
# # pImage.fromarray(array).save(fname)
# fname='dwaynejohnson.jpg'

# label_list = ['eye','na']
# result_dict = {'points':[[0,0]],'labels':[1]}

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
#     os.remove(fname)
#     st.rerun()

from glob import glob
import pandas as pd
import streamlit as st
from streamlit_image_annotation import classification

label_list = ['deer', 'human', 'dog', 'penguin', 'framingo', 'teddy bear']
image_path_list = glob('image/*.jpg')
if 'result_df' not in st.session_state:
    st.session_state['result_df'] = pd.DataFrame.from_dict({'image': image_path_list, 'label': [0]*len(image_path_list)}).copy()

num_page = st.slider('page', 0, len(image_path_list)-1, 0)

label = classification(image_path_list[num_page], 
                        label_list=label_list, 
                        default_label_index=int(st.session_state['result_df'].loc[num_page, 'label']))

if label is not None and label['label'] != st.session_state['result_df'].loc[num_page, 'label']:
    st.session_state['result_df'].loc[num_page, 'label'] = label_list.index(label['label'])
st.table(st.session_state['result_df'])