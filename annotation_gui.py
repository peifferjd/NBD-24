import streamlit as st
import numpy as np
import datajoint as dj
# dj.config['database.host'] = st.secrets['datajoint']['HOST']
# dj.config['database.user'] = st.secrets['datajoint']['USER']
# dj.config['database.password'] = st.secrets['datajoint']['PASS']

from annotation_schema import CroppedImage, CroppedImageLabel
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

st.set_page_config(
    page_title="Eye Annotation Tool!",
    page_icon="🧊")
st.markdown('Click on both eyes. Then click "Next".')
st.markdown('If you mess up, keep clicking. Or refresh page.')
def get_ellipse_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
    center = point
    radius = 10
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )

keys = CroppedImage.fetch('KEY')

if "points" not in st.session_state:
    st.session_state["points"] = []
if "key" not in st.session_state:
    st.session_state["key"] = keys[0]
if "new_image_selected" not in st.session_state:
    st.session_state["new_image_selected"] = False  # Flag to indicate a new image was selected

# Submit button to choose a random filename and clear points
if st.button('Next'):
    key = st.session_state["key"]
    ordered = sorted(st.session_state['points'], key=lambda x: x[0], reverse=True)
    key.update({'y':np.array(ordered).reshape(1,4)//4})
    CroppedImageLabel.insert1(key)
    st.session_state["key"] = np.random.choice(keys)
    st.write(st.session_state["key"])
    st.session_state["points"].clear()
    st.session_state["new_image_selected"] = True  # Set the flag to True

with Image.fromarray((CroppedImage & st.session_state['key']).fetch1('image_cropped')).resize((256,256),Image.BICUBIC) as img:
    draw = ImageDraw.Draw(img)

    # Draw an ellipse at each coordinate in the last two points
    for point in st.session_state["points"][-2:]:
        coords = get_ellipse_coords(point)
        draw.ellipse(coords, fill="red")

    value = streamlit_image_coordinates(img, key="pil")


    if value is not None and not st.session_state["new_image_selected"]:  # Check the flag before adding a new point
        point = (value["x"], value["y"])
        if point not in st.session_state["points"]:
            if len(st.session_state["points"]) >= 2:
                st.session_state["points"].pop(0)
            st.session_state["points"].append(point)
            st.experimental_rerun()

    st.session_state["new_image_selected"] = False 