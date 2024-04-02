import datajoint as dj
import matplotlib.pyplot as plt

schema = dj.schema('nbd')


@schema
class Image(dj.Manual):
    definition = """
    fname: varchar(255)
    ---
    image: longblob
    """
    def show(self):
        fig = plt.figure()
        axs = fig.add_subplot(111)
        axs.imshow(self.fetch1('image'))
        return axs

@schema
class CroppedImage(dj.Computed):
    definition = """
    -> Image
    ---
    image: longblob
    x: int
    y: int
    width: int
    height: int
    """
    def make(self,key):
        import cv2

        img = cv2.imread('faces_unannotated/'+key['fname'])
        # Convert the image to grayscale - Haar Cascades require grayscale images
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        print(faces)
        assert faces is not None, 'No face detected.'
        assert faces.shape[0] == 1, 'More than one face detected.'

        x, y, w, h = faces[0]

        face_img = gray[y:y+h, x:x+w]
        resized_face = cv2.resize(face_img, (64, 64))

        key['image'] = resized_face
        key['x'] = x
        key['y'] = y
        key['width'] = w
        key['height'] = h

        self.insert1(key)
    
    def show(self):
        fig = plt.figure()
        axs = fig.add_subplot(111)
        axs.imshow(self.fetch1('image'))
        return axs

@schema
class Label(dj.Manual):
    definition = """
    -> Image
    annotation_timestamp: datetime
    ---
    label:  longblob
    """
