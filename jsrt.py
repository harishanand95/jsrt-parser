import numpy as np
# from scipy.misc import imresize, imread
import matplotlib.pyplot as plt
# import csv
from os import listdir


class JsrtImage(object):
    """ JSRTImage object provides the image and its descriptions in a bundled format. Descriptions for the image include
     filename, nodule size [mm], degree of subtlety, x and y coordinates of the nodule location, age, sex, malignant
      or benign, anatomic location, and diagnosis. """

    def __init__(self, path):
        self.image = None
        self.image_path = path
        self.image_height = None
        self.image_width = None
        self._image_type = None
        self._malignant_or_benign = None
        self._nodule_size = None
        self._degree_of_subtlety = None
        self._x_coordinate = None
        self._y_coordinate = None
        self._diagnosis = None
        self.load()

    def load(self):
        """ Image is of size 2048x2048 in gray scale stored in 16 bit unsigned int in big endian format. """
        raw_image = np.fromfile(self.image_path, dtype=">i2").reshape((2048, 2048))
        raw_image.shape = (2048, 2048)
        self.image = raw_image
        self.image_height = 2048
        self.image_width = 2048
        return self

    @property
    def image_type(self):
        if "JPCLN" in self.image_path:
            self._image_type = "has-nodule"
        else:
            self._image_type = "non-nodule"
        return self._image_type

    def display(self):
        plt.imshow(self.image, cmap=plt.get_cmap('gray'))
        plt.show()
        return self


class Jsrt(object):
    """ JSRT is a model to fetch all the images and augment them. """

    def __init__(self, images_path):
        self._images_dir = images_path
        self._has_nodule_image_list = None
        self._non_nodule_image_list = None
        self.__get_images_list()

    def __get_images_list(self):
        images_list = listdir(self._images_dir)
        _has_nodule_files = []
        _non_nodule_files = []
        # Non-nodule and has-nodule filename are separated based on filename.
        for filename in images_list:
            if "JPCLN" in filename:
                _has_nodule_files.append(filename)
            else:
                _non_nodule_files.append(filename)
        # Image objects are stored as list on _has_nodule_image_list and _non_nodule_image_list
        self._has_nodule_image_list = self._load_images_from_file(_has_nodule_files, self._images_dir)
        self._non_nodule_image_list = self._load_images_from_file(_non_nodule_files, self._images_dir)
        return self

    @staticmethod
    def _load_images_from_file(filenames, directory):
        """ _load_images_from_file loads images located at folder + filename into a list of JsrtImage objects.
            Input  : filenames - a list of image file names
                     directory - path to the directory where all images are present
            Output : [JsrtImage objects]
        """
        images_list = []
        for image_path in filenames:
            img = JsrtImage(directory + image_path)
            images_list.append(img)
        return images_list

    def get_images(self, has_nodule=True, num_of_images=1):
        """ get_images function returns "num_of_images" number of JsrtImage objects in a list.
        Function takes a bool has_nodule which return images with nodules when True and non-nodule images when False.
        Input  : has_nodule (defaults to True), num_of_images (defaults to 1).
        Output : [JsrtImage object]
        """
        if has_nodule is True:
            if len(self._has_nodule_image_list) < num_of_images:
                print "Number of images available is " + str(len(self._has_nodule_image_list))
                return -1
            return self._has_nodule_image_list[:num_of_images]
        else:
            if len(self._has_nodule_image_list) < num_of_images:
                print "Number of images available is " + str(len(self._non_nodule_image_list))
                return -1
            return self._non_nodule_image_list[:num_of_images]


dataset = Jsrt("./All247images/")
image = dataset.get_images()
image[0].display()