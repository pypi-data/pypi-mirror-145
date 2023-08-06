"""
This module is used to easily read and view images from your dataset. A fast way of checking how the data is before doing anything with it.
"""

from easyaug.quickview import read
from easyaug.quickview import view

class Quickviewer:
    """
    A class used to read and view images. When created an instance of it allows you to access the functions that reads
    the images or image names by specifying the path to your data. Then view the images in a plot or the image names in
    the terminal.

    Parameters
    ----------

    Examples
    --------
    >>> from easyaug.quickview import Quickviewer
    >>> viewer = Quickviewer()
    Initializing viewer...
    """

    def __init__(self):
        self.images = []
        self.imagenames = []

    def read_all_images(self, path, type_of_image=None):
        """
        A function that reads all the images in the specified path. If the type_of_image is specified, it will only read the images of that type.

        Parameters
        ----------
        path : str
            The path to your data.
        type_of_image : str
            The type of images you want to read. Set to None as default.

        Raises
        ------
        ValueError
            If there are no images in the specified path.

        Returns
        -------
        images : list
            A list of the images.

        Examples
        --------
        >>> from easyaug.quickview import Quickviewer
        >>> viewer = Quickviewer()
        >>> viewer.read_all_images('/home/user/data/', 'png')
        Reading all images of type png...


        """

        self.images = read.read_all_images(path, type_of_image)
        read.no_images_error_handling(len(self.images))
        print("Read", len(self.images), "images.")
        return self.images



    def read_every_x_image(self, path, x, type_of_image=None):
        """
        A function that reads every x images in the specified path. If the type_of_image is specified, it will only read the images of that type.

        Parameters
        ----------
        path : str
            The path to your data.
        x : int
            For every number of image you want to read.
        type_of_image : str
            The type of images you want to read. Set to None as default.

        Raises
        ------
        ValueError
            If there are no images in the specified path.
            If there are less images than x.
            If x is less than 1.
            If x is not an integer.

        Returns
        -------
        images : list
            A list of the images.

        Examples
        --------
        >>> from easyaug.quickview import Quickviewer
        >>> viewer = Quickviewer()
        >>> viewer.read_every_x_image('/home/user/data/', 5, 'png')
        Reading every 5 images of type png...
        """

        self.images = read.read_every_x_image(path, x, type_of_image)
        read.no_images_error_handling(len(self.images))
        print("Read", len(self.images), "images.")
        return self.images

    def read_first_x_images(self, path, x, type_of_image=None):
        """
        A function that reads the first x images in the specified path. If the type_of_image is specified, it will only read the images of that type.

        Parameters
        ----------
        path : str
            The path to your data.
        x : int
            The first number of images you want to read.
        type_of_image : str
            The type of images you want to read. Set to None as default.

        Raises
        ------
        ValueError
            If there are no images in the specified path.
            If there are less images than x.
            If x is less than 1.
            If x is not an integer.

        Returns
        -------
        images : list
            A list of the images.

        Examples
        --------
        >>> from easyaug.quickview import Quickviewer
        >>> viewer = Quickviewer()
        >>> viewer.read_first_x_images('/home/user/data/', 5, 'png')
        Reading first 5 images of type png...

        """
        self.images = read.read_first_x_images(path, x, type_of_image)
        read.no_images_error_handling(len(self.images))
        print("Read", len(self.images), "images.")
        return self.images

    def read_last_x_images(self, path, x, type_of_image=None):
        """
        A function that reads the last x images in the specified path. If the type_of_image is specified, it will only read the images of that type.

        Parameters
        ----------
        path : str
            The path to your data.
        x : int
            The last number of images you want to read.
        type_of_image : str
            The type of images you want to read. Set to None as default.

        Raises
        ------
        ValueError
            If there are no images in the specified path.
            If there are less images than x.
            If x is less than 1.
            If x is not an integer.

        Returns
        -------
        images : list
            A list of the images.

        Examples
        --------
        >>> from easyaug.quickview import Quickviewer
        >>> viewer = Quickviewer()
        >>> viewer.read_last_x_images('/home/user/data/', 5, 'png')
        Reading last 5 images of type png...
        """
        self.images = read.read_last_x_images(path, x, type_of_image)
        read.no_images_error_handling(len(self.images))
        print("Read", len(self.images), "images.")
        return self.images

    def read_a_image(self, path):
        """
        A function that reads a single image in the specified path.

        Parameters
        ----------
        path : str
            The path to your data.

        Raises
        ------
        ValueError
            If there are no images in the specified path.

        Returns
        -------
        images : list
            A list of the images.

        Examples
        --------
        >>> from easyaug.quickview import Quickviewer
        >>> viewer = Quickviewer()
        >>> viewer.read_a_image('/home/user/data/')
        Reading a image...
        """
        self.images.append(read.read_a_image(path))
        read.no_images_error_handling(len(self.images))
        print("Read 1 image.")
        return self.images

    def read_all_imagenames(self, path, type_of_image=None):
        """
        A function that reads all the image names in the specified path. If the type_of_image is specified, it will only read the images of that type.

        Parameters
        ----------
        path : str
            The path to your data.
        type_of_image : str
            The type of images you want to read the name of. Set to None as default.

        Raises
        ------
        ValueError
            If there are no images in the specified path.

        Returns
        -------
        imagenames : list

        Examples
        --------
        >>> from easyaug.quickview import Quickviewer
        >>> viewer = Quickviewer()
        >>> viewer.read_all_imagenames('/home/user/data/', 'png')
        Reading all image names of type png...
        """
        self.imagenames = read.read_all_imagenames(path, type_of_image)
        read.no_images_error_handling(len(self.imagenames))
        print("Read", len(self.imagenames), "imagenames.")
        return self.imagenames


    def read_every_x_imagename(self, path, x, type_of_image=None):
        """
        A function that reads every x image name in the specified path. If the type_of_image is specified, it will only read the images of that type.

        Parameters
        ----------
        path : str
            The path to your data.
        x : int
            For every number of image names you want to read.
        type_of_image : str
            The type of images you want to read the name of. Set to None as default.

        Raises
        ------
        ValueError
            If there are no images in the specified path.
            If there are less images than x.
            If x is less than 1.
            If x is not an integer.

        Returns
        -------
        imagenames : list
            A list of the image names.

        Examples
        --------
        >>> from easyaug.quickview import Quickviewer
        >>> viewer = Quickviewer()
        >>> viewer.read_every_x_imagename('/home/user/data/', 5, 'png')
        Reading every 5 image names of type png...
        """
        self.imagenames = read.read_every_x_imagename(path, x, type_of_image)
        read.no_images_error_handling(len(self.imagenames))
        print("Read", len(self.imagenames), "imagenames.")
        return self.imagenames


    def read_first_x_imagenames(self, path, x, type_of_image=None):
        """
        A function that reads the first x image names in the specified path. If the type_of_image is specified, it will only read the images of that type.

        Parameters
        ----------
        path : str
            The path to your data.
        x : int
            The first number of image names you want to read.
        type_of_image : str
            The type of images you want to read the name of. Set to None as default.

        Raises
        ------
        ValueError
            If there are no images in the specified path.
            If there are less images than x.
            If x is less than 1.
            If x is not an integer.

        Returns
        -------
        imagenames : list
            A list of the image names.

        Examples
        --------
        >>> from easyaug.quickview import Quickviewer
        >>> viewer = Quickviewer()
        >>> viewer.read_first_x_imagenames('/home/user/data/', 5, 'png')
        Reading first 5 image names of type png...
        """
        self.imagenames = read.read_first_x_imagenames(path, x, type_of_image)
        read.no_images_error_handling(len(self.imagenames))
        print("Read", len(self.imagenames), "imagenames.")
        return self.imagenames

    def read_last_x_imagenames(self, path, x, type_of_image=None):
        """
        A function that reads the last x image names in the specified path. If the type_of_image is specified, it will only read the images of that type.

        Parameters
        ----------
        path : str
            The path to your data.
        x : int
            The last number of image names you want to read.
        type_of_image : str
            The type of images you want to read the name of. Set to None as default.

        Raises
        ------
        ValueError
            If there are no images in the specified path.
            If there are less images than x.
            If x is less than 1.
            If x is not an integer.

        Returns
        -------
        imagenames : list
            A list of the image names.

        Examples
        --------
        >>> from easyaug.quickview import Quickviewer
        >>> viewer = Quickviewer()
        >>> viewer.read_last_x_imagenames('/home/user/data/', 5, 'png')
        Reading last 5 image names of type png...
        """
        self.imagenames = read.read_last_x_imagenames(path, x, type_of_image)
        read.no_images_error_handling(len(self.imagenames))
        print("Read", len(self.imagenames), "imagenames.")
        return self.imagenames


    def view_images(self, maximum=9, images=None):
        """
        A function that plots the read images in a grid. If the images parameter is specified, it will plot the last images you read.
        It will only plot the first 9 images in the list as default.

        Parameters
        ----------
        maximum : int
            The maximum number of images you want to plot. Set to 9 as default.
        images : list
            A list of the images you want to plot. Set to None as default.

        Raises
        ------
        ValueError
            If there are no images in the list or stored from previous reads.
            If the maximum is less than 1.
            If the maximum is not an integer.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.quickview import Quickviewer
        >>> viewer = Quickviewer()
        >>> viewer.read_first_x_imagenames('/home/user/data/', 5, 'png')
        >>> viewer.view_images()
        Viewing first 5 images of type png...
        """

        if not isinstance(maximum, int):
            raise ValueError("Maximum must be an integer.")
        if maximum < 1:
            raise ValueError("Maximum must be greater than 0.")
        if images is not None:
            read.no_images_error_handling(len(images))
            view.view_images(images, maximum)
        elif len(self.images) != 0:
            view.view_images(self.images, maximum)
        else:
            raise ValueError("No images found.")

    def view_imagenames(self, maximum=20, imagenames=None):
        """
        A function that prints the read image names or the names of the read images in the terminal.
        If the imagenames parameter is specified, it will print the last imagenames or names of images you read.
        It will only print the first 20 imagenames in the list as default.

        Parameters
        ----------
        maximum : int
            The maximum number of imagenames you want to print. Set to 20 as default.
        imagenames : list
            A list of the imagenames you want to print. Set to None as default.

        Raises
        ------
        ValueError
            If there are no imagenames in the list or stored from previous reads.
            If the maximum is less than 1.
            If the maximum is not an integer.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.quickview import Quickviewer
        >>> viewer = Quickviewer()
        >>> viewer.read_first_x_imagenames('/home/user/data/', 5, 'png')
        >>> viewer.view_imagenames()
        Viewing first 5 imagenames of type png...

        """
        if not isinstance(maximum, int):
            raise ValueError("Maximum must be an integer.")
        if maximum < 1:
            raise ValueError("Maximum must be greater than 0.")
        if imagenames is not None:
            read.no_images_error_handling(len(imagenames))
            view.view_imagesnames(imagenames, maximum)
        elif len(self.imagenames) != 0:
            view.view_imagesnames(self.imagenames, maximum)
        elif len(self.images) != 0:
            view.view_imagesnames_from_images(self.images, maximum)
        else:
            raise ValueError("No imagenames or images found.")






