import numpy as np
# from scipy.misc import imresize, imread
import matplotlib.pyplot as plt
from csv import reader, excel_tab
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
        self._age = None
        self._sex = None
        self._position = None
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

    @image_type.setter
    def image_type(self, value):
        self._image_type = value

    def display(self):
        plt.imshow(self.image, cmap=plt.get_cmap('gray'))
        plt.show()
        return self

    # def display_all_data(self):
    #     print self._degree_of_subtlety
    #     print self._nodule_size
    #     print self._age
    #     print self._sex
    #     print self._x_coordinate
    #     print self._y_coordinate
    #     print self._malignant_or_benign
    #     print self._position
    #     print self._diagnosis

    def add_description(self, data, has_nodule=False):
        """This function adds additional details to the JsrtImage object.

        Args:
            data       (list): data is a list of the form [filename, degree of subtlety, nodule size [mm], age, sex,
                               x coordinate of the nodule, y coordinate of the nodule, pathology, position, diagnosis]
                               for images with nodules and [filename, age, sex, diagnosis("non-nodule")] for non-nodule
                               images respectively.
            has_nodule (bool): True for images with nodules and False for images without nodules.
        """
        if has_nodule is True:
            self.image_type = "has nodule"
            self._degree_of_subtlety = data[1]
            self._nodule_size = data[2]
            self._age = data[3]
            self._sex = data[4]
            self._x_coordinate = data[5]
            self._y_coordinate = data[6]
            self._malignant_or_benign = data[7]
            self._position = data[8]
            self._diagnosis = data[9]

        elif has_nodule is False:
            self._image_type = "non-nodule"
            self._age = data[1]
            self._sex = data[2]


class Jsrt(object):
    """ JSRT is a model to fetch all the images and augment them. """

    def __init__(self, images_path):
        self._images_dir = images_path
        self._has_nodule_image_list = None
        self._non_nodule_image_list = None
        self.__get_images_list()
        self.add_descriptions_to_image()

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
        """This function load images (not image) located at directory/filename and creates an image object from it.
        Args:
            filenames (list): a list of names of the image files.
            directory  (str): path to the directory/folder where all images are present
        Returns :
            a list of JsrtImage objects
        """
        images_list = []
        for image_name in filenames:
            img = JsrtImage(directory + image_name)
            images_list.append(img)
        return images_list

    def clean_csv_file(self, file_path, file_type):
        """This function cleans the csv data present along with the image file. The data is removed of inappropriate
        splits and combined into a 10 element list for images with nodules and 4 element list for images without
        nodules.
        csv content is formatted into [filename, degree of subtlety, nodule size [mm], age, sex, x coordinate
        of the nodule, y coordinate of the nodule, pathology, position, diagnosis] format for images with nodules
        and [filename, age, sex, diagnosis("non-nodule")] format for non-nodule images respectively.

        Args:
            file_path (str) : Path to the CSV file for nodule and non-nodule images.
            file_type (str) : If file_path is to nodule images, then file_type is "nodule csv" and if file_path is to
                              non-nodule images, then file_type is "non nodule csv".

        Returns:
            csv_data (dict): csv_data returns a dict of the form { 'filename' : 'filename' image's csv data }.

            Example:
                { "./All247images/JPCNN010.IMG" : ['JPCNN010.IMG', '54', 'male', 'non-nodule'] }

        """
        csv_data = {}
        if file_type == "nodule csv":
            with open(file_path, "rU") as csv_file:
                content = reader(csv_file, dialect=excel_tab)
                for row in content:
                    if len(row) != 0:
                        row[8:10] = [" ".join(row[8:10])]
                        row[9:] = [" ".join(row[9:])]
                        csv_data[self._images_dir + row[0]] = row
            return csv_data
        elif file_type == "non nodule csv":
            with open(file_path, "rU") as csv_file:
                content = reader(csv_file, dialect=excel_tab)
                for row in content:
                    if len(row) != 0:
                        row = row[0].split(" ")
                        new_row = []
                        new_row.extend([row[0], row[1], row[3], row[len(row) - 1]])
                        csv_data[self._images_dir + new_row[0]] = new_row
            return csv_data
        else:
            return csv_data

    def add_descriptions_to_image(self):
        """ This function fetches the descriptions of the images present in the csv file and adds them
            to the JsrtImage object.
        """
        csv_data = self.clean_csv_file("Clinical_Information/CLNDAT_EN.txt", "nodule csv")

        for image in self._has_nodule_image_list:
            print image.image_path
            print csv_data[image.image_path]
            image.add_description(csv_data[image.image_path], has_nodule=True)

        csv_data = self.clean_csv_file("Clinical_Information/CNNDAT_EN.TXT", "non nodule csv")

        for image in self._non_nodule_image_list:
            print image.image_path
            print csv_data[image.image_path]
            image.add_description(csv_data[image.image_path], has_nodule=False)

    def get_images(self, has_nodule=True, num_of_images=1):
        """This function gives "num_of_images" number of JsrtImage objects in a list. The objects can be either all
        image with nodules or non-nodules.

        Args:
            has_nodule   (bool): Defaults to True. Images with the nodules are selected when it is set to True and
                                images without nodules are selected when it is set to False.
            num_of_images (int): Defaults to 1. The required number of images is given.

        Returns :
            a list of JsrtImage objects. Total objects will be num_of_images.
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
pic = dataset.get_images()
# pic[0].display_all_data()

