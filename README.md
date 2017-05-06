# jsrt-parser
This is a data parser to obtain images and descriptions from JSRT database in a uniform format for deep learning applications.

Expected features:
- [ ]  Scale, rotate and resize images to augment the dataset.

        The training and validation sets will be augmented by applying a number of image transformations: 
            1. Horizontal reflection
            2. Rotation by 2°-10°
            3. Translation of 3 pixels in cardinal or ordinal directions (Optional: not sure of its consequence to image)
            4. Pixel spread (swap each pixel with a random adjacent pixel)
            5. Noise reduction (replace each pixel with the value just before or after the median value in a neighborhood of 2 or 5 pixels)
            6. Random noise addition.
            
     In total, each image can serve as the progenitor of 106 child images with the label inherited from the parent image. 
     
     This is an attempt to augment the images similar to the one mentioned in High-Throughput Classification of Radiographs Using Deep Convolutional Neural Networks by Alvin Rajkomar & Sneha Lingam & Andrew G. Taylor & Michael Blum & John Mongan.
     
     https://link.springer.com/article/10.1007/s10278-016-9914-9


- [ ]  Get random X type of images or just a random mix of images from dataset.
- [x]  Get image description and other attributes associated with each image.

        img = JsrtImage()
        img.load_from_file("./All247images/JPCNN010.IMG")
        img.add_description(['JPCNN010.IMG', '54', 'male', 'non-nodule'], has_nodule=False)
        print img.image_type
        print img.image_width
        print img.image_height
   
- [x]  Display image with a marking over the location of lung nodule.

        img.display()
      
    ![picture alt](https://raw.githubusercontent.com/harishanand95/jsrt-parser/master/test_image.png "lung nodule marked")
- [ ]  Implement a method to find new location of the nodule during an image's horizontal flip.
- [x]  Option to load and save the images into a binary format.

        jsrtdata = Jsrt().load_images("./All247images/")
        save_pic = jsrtdata.get_images(num_of_images=1)
        # write image to test.tfrecords
        jsrtdata.save_images(save_pic, "test.tfrecords")
        
        # read image from test.tfrecords
        read_pic = jsrtdata.read_images("test.tfrecords")
        
        # compare of saved image and read image
        print np.allclose(save_pic[0].image, read_pic[0].image)
        
        if save_pic[0].image_height == read_pic[0].image_height: print "True"
        if save_pic[0].image_width == read_pic[0].image_width: print "True"
        if save_pic[0].x == read_pic[0].x: print "True"
        if save_pic[0].y == read_pic[0].y: print "True"
        
        # You should get 5 True statement as results, which confirms that the values are same.
- [ ]  Separate out test dataset from train and validation set.
- [ ]  (Optional) Implement a method to get a zoomed portion of the image given the coordinates to zoom and image size. Required for attention based models.
