"""
A module to preprocess images if needed.
"""

from easyaug.preprocess import resize

class Preprocesser:
    """
    A class to use different preprocessing methods.
    """
    def __init__(self):
        self.input_path = None
        self.output_path = None
        self.type_of_image = None

    def specify_input_and_output_path(self, input_path, output_path, type_of_image=None):
        """
        Specify the path to the data.

        Parameters
        ----------
        input_path : str
            The path to the folder where the images are.
        output_path : str
            The path to the folder where the images will be saved.
        type_of_image : str
            The type of the image you want to augment.

        Raises
        ------
        ValueError
            If the input_path or output_path is not a string.
            If the input_path or output_path is not specified.
            If type_of_image is not None, "jpg" og "png".

        Returns
        -------

        Examples
        --------
        >>> from easyaug.preprocess import Preprocesser
        >>> processer = Preprocesser()
        >>> processer.specify_input_and_output_path("/path/to/input/folder", "/path/to/output/folder", "jpg")
        Specified input path, output path and type of image to be preprocessed.
        """

        if type_of_image is not None:
            if type_of_image != "jpg" and type_of_image != "png" and type_of_image != "PNG" and type_of_image != "JPG":
                raise ValueError("Type of image must be None, jpg or png")
        if input_path is None or output_path is None:
            raise ValueError("No path specified")
        elif type(input_path) is not str or type(output_path) is not str:
            raise ValueError("Path must be a string")
        else:
            self.input_path = input_path
            self.output_path = output_path
            self.type_of_image = type_of_image

    def run_resize(self, size=(256, 256)):
        """
        A simple method to resize the images. Only resizes the images to the specified folder. Does not iterate through down the directory tree.

        Parameters
        ----------
        size : tuple
            The size of the image.

        Raises
        ------
        ValueError
            If the input_path or output_path is not specified.
            If the size is not a tuple.
            If the size is not specified.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.preprocess import Preprocesser
        >>> processer = Preprocesser()
        >>> processer.specify_input_and_output_path("/path/to/input/folder", "/path/to/output/folder", "jpg")
        >>> processer.run_resize((256, 256))
        Resized images from the specified folder.
        """
        if self.input_path is None:
            raise ValueError("No path specified")
        # If size is not tuple raise error
        if type(size) is not tuple:
            raise ValueError("Size must be a tuple")
        else:
            resize.resize(self.input_path, self.output_path, self.type_of_image, size)

