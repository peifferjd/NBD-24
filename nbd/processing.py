import cv2
import numpy as np

def auto_crop_and_resize_face(image):
    """
    Automatically detects faces in the image, crops the first detected face,
    resizes it to 64x64 pixels, and returns the cropped and resized face along with
    the updated coordinates in the original image.

    Parameters:
    - image: A grayscale image as a NumPy array.

    Returns:
    - resized_face: The cropped and resized face.
    - face_coords: The coordinates of the detected face in the original image.
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Load the pre-trained Haar Cascade model for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    
    if len(faces) == 0:
        return None, None  # No faces detected
    
    # Assuming the first detected face is the one we want
    x, y, w, h = faces[0]
    
    # Crop the face
    cropped_face = image[y:y+h, x:x+w]
    
    # Resize the face to 64x64
    resized_face = cv2.resize(cropped_face, (64, 64))
    
    # The coordinates of the detected face in the original image
    face_coords = np.array([x, y, x+w, y+h])
    
    return resized_face, face_coords

def transform_points(face_coords, y, resized_size=(64, 64)):
    """
    Transform points from original image coordinates to cropped and resized image coordinates,
    given the face bounding box and original points.
    
    Parameters:
    - face_coords: A 1D array with [x1, y1, x2, y2] representing the face bounding box in the original image.
    - y: A 2D array with [[x1, y1, x2, y2]] representing two points in the original image.
    - resized_size: The size (height, width) of the resized image. Default is (64, 64).
    
    Returns:
    - transformed_points: A 2D array with [[x1, y1, x2, y2]] with transformed points in the resized image coordinates.
    """
    # Calculate the scale factors for x and y dimensions
    scale_x = resized_size[1] / (face_coords[2] - face_coords[0])
    scale_y = resized_size[0] / (face_coords[3] - face_coords[1])
    
    # Adjust y points to be relative to the top-left corner of the face bounding box
    # Reshape face_coords[:2] for broadcasting
    adjusted_y = (y.reshape(-1,2) - face_coords[:2]).reshape(1,4)

    # Apply scaling to adjust the points to the resized image dimensions
    transformed_points = adjusted_y * np.array([scale_x, scale_y, scale_x, scale_y])
    
    # Ensure the output is rounded and cast to int for pixel coordinates
    transformed_points = np.round(transformed_points).astype(int)
    
    return transformed_points

