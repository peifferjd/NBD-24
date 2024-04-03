import streamlit as st
import numpy as np
from annotation_schema import CroppedImageLabel,CroppedImage

key = np.random.choice((CroppedImage & CroppedImageLabel).fetch('KEY'),2)

col1, col2 = st.columns(2)

with col1:
    plot = (CroppedImageLabel & key[0]).showall()
    st.pyplot(plot)
    st.write(key[0])
with col2:
    plot = (CroppedImageLabel & key[1]).showall()
    st.pyplot(plot)
    st.write(key[1])