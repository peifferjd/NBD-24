import datajoint as dj
import matplotlib.pyplot as plt

schema = dj.schema('nbd')


@schema
class DatasetImage(dj.Manual):
    definition = """
    fname: varchar(255)
    ---
    image: longblob
    y: longblob
    """
    def show(self):
        fig = plt.figure()
        axs = fig.add_subplot(111)
        axs.imshow(self.fetch1('image'))
        y = self.fetch1('y').reshape(-1, 2)
        axs.scatter(y[:, 0], y[:, 1], c='r')
        return fig
    
    


@schema
class CroppedDatasetImage(dj.Computed):
    definition = """
    -> DatasetImage
    ---
    image_cropped: longblob
    y_cropped: longblob
    crop_x1: int
    crop_y1: int
    crop_x2: int
    crop_y2: int
    """
    def make(self,key):
        from processing import auto_crop_and_resize_face, transform_points

        image, y = (DatasetImage & key).fetch1('image', 'y')
        resized, face_coords = auto_crop_and_resize_face(image)
        new_y = transform_points(face_coords, y)

        key['image_cropped'] = resized 
        key['y_cropped'] = new_y
        key['crop_x1'], key['crop_y1'], key['crop_x2'], key['crop_y2'] = face_coords
        self.insert1(key)
    
    def show(self):
        fig = plt.figure()
        axs = fig.add_subplot(111)
        axs.imshow(self.fetch1('image_cropped'))
        y = self.fetch1('y_cropped').reshape(-1, 2)
        axs.scatter(y[:, 0], y[:, 1], c=['r','y'])
        return fig

@schema
class UnannotatedImage(dj.Manual):
    definition = """
    fname: varchar(255)
    ---
    image: longblob
    """
    def show(self):
        fig = plt.figure()
        axs = fig.add_subplot(111)
        axs.imshow(self.fetch1('image'))
        return fig
    
@schema
class CroppedImage(dj.Computed):
    definition = """
    -> UnannotatedImage
    ---
    image_cropped: longblob
    crop_x1: int
    crop_y1: int
    crop_x2: int
    crop_y2: int
    """
    def make(self,key):
        from processing import auto_crop_and_resize_face

        image = (UnannotatedImage & key).fetch1('image')
        resized, face_coords = auto_crop_and_resize_face(image)

        key['image_cropped'] = resized 
        key['crop_x1'], key['crop_y1'], key['crop_x2'], key['crop_y2'] = face_coords
        self.insert1(key)

    def show(self):
        fig = plt.figure()
        axs = fig.add_subplot(111)
        axs.imshow(self.fetch1('image_cropped'))
        return fig

@schema
class CroppedImageLabel(dj.Manual):
    definition = """
    -> CroppedImage
    entry_time = CURRENT_TIMESTAMP : timestamp 
    ---
    y: longblob
    """
    def show(self):
        fig = plt.figure()
        axs = fig.add_subplot(111)
        axs.imshow((CroppedImage & self).fetch1('image_cropped'))
        y = self.fetch1('y').reshape(-1, 2)
        axs.scatter(y[:, 0], y[:, 1], c=['r','y'])
        # return fig
    
    def showall(self):
        fig = plt.figure()
        axs = fig.add_subplot(111)
        axs.imshow((CroppedImage & self).fetch1('image_cropped'))
        for y in self.fetch('y'):
            y = y.reshape(-1, 2)
            axs.scatter(y[:, 0], y[:, 1], c=['r','y'])
