import numpy as np
from scipy.misc import imresize, imread
import matplotlib.pyplot as plt


class JSRTImage(object):
    """ JSRTImage object provides the image and its descriptions in a bundled format. Descriptions for the image include
     filename, nodule size [mm], degree of subtlety, x and y coordinates of the nodule location, age, sex, malignant
      or benign, anatomic location, and diagnosis. """
    def __init__(self, path):
        self.image = None
        self.image_path = path
        self.image_height = None
        self.image_width = None
        self._image_type = None
        self._nodule_size = None
        self._degree_of_subtlety = None
        self._x_coordinate = None
        self._y_coordinate = None
        self._diagnosis = None

    def load(self):
        """ Image is of size 2048x2048 in gray scale stored in 16 bit unsigned int in big endian format. """
        raw_image = np.fromfile(self.image_path, dtype=">i2").reshape((2048, 2048))
        raw_image.shape = (2048, 2048)
        self.image = raw_image
        self.image_height = 2048
        self.image_width = 2048
        return self

    def display(self):
        plt.imshow(self.image, cmap=plt.get_cmap('gray'))
        plt.show()
        return self


# class JSRT(object):
#     """ JSRT is a model to fetch all the images and augment them"""
#     def __init__(self, images_path):
#         self._images_folder = images_path


img = JSRTImage("./All247images/JPCLN002.IMG")
img.load().display()