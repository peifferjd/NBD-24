import streamlit as st
from streamlit_image_annotation import pointdet
from annotation_schema import Image, Label
import numpy as np



fname = np.random.choice(Image.fetch('fname'))

label_list = ['eye','na']
result_dict = {'points':[[0,0]],'labels':[1]}

new_labels = pointdet(image_path='faces_unannotated/'+fname, 
                        label_list=label_list, 
                        points=result_dict['points'],
                        labels=result_dict['labels'],
                        key=fname)
if new_labels is not None:
    result_dict['points'] = [v['point'] for v in new_labels]
    result_dict['labels'] = [v['label_id'] for v in new_labels]
    st.json(result_dict)
    st.rerun()