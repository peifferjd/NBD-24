import streamlit as st
from PIL import Image as pImage
import tempfile
import numpy as np
import os





import streamlit as st
import numpy as np
from annotation_schema import CroppedImage
from streamlit_image_coordinates import streamlit_image_coordinates
import os

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

key = np.random.choice(CroppedImage.fetch("KEY"))
array = (CroppedImage & key).fetch1("image_cropped")
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