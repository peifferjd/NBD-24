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
    def image(self):
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
