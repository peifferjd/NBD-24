import os
import numpy as np
import datajoint as dj
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from PIL import Image, ImageDraw
import base64
import io
import json
import time
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure DataJoint
# You'll need to set these as environment variables or in a config file
# dj.config['database.host'] = os.environ.get('DJ_HOST')
# dj.config['database.user'] = os.environ.get('DJ_USER')
# dj.config['database.password'] = os.environ.get('DJ_PASS')

# Set numpy random seed based on time
np.random.seed(int(time.time()) % 1000)

# Import your schema
from annotation_schema import CroppedImage, CroppedImageLabel

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, 
    x_for=1,         # X-Forwarded-For
    x_proto=1,       # X-Forwarded-Proto
    x_host=1,        # X-Forwarded-Host
    x_prefix=1,      # X-Forwarded-Prefix
    x_port=1         # X-Forwarded-Port
)
app.config['PREFERRED_URL_SCHEME'] = 'http'
app.secret_key = 'your_secret_key'  # Set a secure secret key for sessions

def get_ellipse_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
    center = point
    radius = 10
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )

def get_random_image_key():
    keys = CroppedImage.fetch('KEY')
    return np.random.choice(keys)

def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

@app.route('/')
def index():
    # Initialize session if needed
    if 'points' not in session:
        session['points'] = []
    if 'key' not in session:
        session['key'] = get_random_image_key()
    
    # Get the image
    key = session['key']
    image_data = (CroppedImage & key).fetch1('image_cropped')
    img = Image.fromarray(image_data).resize((256, 256), Image.BICUBIC)
    
    # Draw ellipses for existing points
    if session['points']:
        draw = ImageDraw.Draw(img)
        for point in session['points'][-2:]:
            coords = get_ellipse_coords(point)
            draw.ellipse(coords, fill="green")
    
    # Convert image for displaying in HTML
    img_b64 = image_to_base64(img)
    
    return render_template('index.html', image=img_b64, points=session['points'])

@app.route('/add_point', methods=['POST'])
def add_point():
    data = request.json
    x = data.get('x')
    y = data.get('y')
    
    if x is not None and y is not None:
        point = (x, y)
        points = session.get('points', [])
        
        # Only keep last 2 points if more are added
        if len(points) >= 2:
            points.pop(0)
        
        points.append(point)
        session['points'] = points
        
    return jsonify(success=True, points=session['points'])

@app.route('/next', methods=['POST'])
def next_image():
    if len(session.get('points', [])) < 2:
        return jsonify(error="Please select both eyes before proceeding.", success=False)
    
    # Save current annotation
    key = session['key']
    ordered = sorted(session['points'], key=lambda x: x[0], reverse=True)
    
    # Convert points to numpy array and reshape
    y_data = np.array(ordered).reshape(1, 4) // 4
    
    # Update key with annotation data
    key_dict = key if isinstance(key, dict) else key.asdict()  # Handle different key formats
    key_dict.update({'y': y_data})
    
    # Insert into database
    CroppedImageLabel.insert1(key_dict)
    
    # Get new random image
    session['key'] = get_random_image_key()
    session['points'] = []
    
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')