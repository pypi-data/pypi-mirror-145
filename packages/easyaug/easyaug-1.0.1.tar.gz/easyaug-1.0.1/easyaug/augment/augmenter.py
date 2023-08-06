"""
This module is used to augment images.
"""

from easyaug.augment import run_view
from easyaug.augment import run_augment
from easyaug.augment import augmenting_types
from imgaug import augmenters as iaa

class Augmenter:
    """
    A class used to augment images. When creating an instance of this class, you can specify the path to your data. Then
    you can specify the augmenting types. These will be set to a todolist. So when finally you choose to either view a few augmented images or augment all images and save them
    to a new directory the todolist will be executed for each image.
    """
    def __init__(self):
        self.input_path = None
        self.output_path = None
        self.type_of_image = None
        self.augmentation_todo = iaa.Sequential() # For each image in the specified path, do the augmenting added to the todo list.
        self.todo_names = [] # Names of each of the augmentation_todo.

    def specify_input_path(self, path, type_of_image=None):
        """
        Specify the path to the data.

        Parameters
        ----------
        path : str
            The path to the folder where the images are.
        type_of_image : str
            The type of the image you want to augment.

        Raises
        ------
        ValueError
            If the path is not a string.
            If the path is not specified.
            If type_of_image is not None, "jpg" og "png".

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.specify_input_path("/home/user/data/", "jpg")
        Specifying path to data: /home/user/data/ and type of image: jpg.
        """

        if type_of_image is not None:
            if type_of_image != "jpg" and type_of_image != "png" and type_of_image != "PNG" and type_of_image != "JPG":
                raise ValueError("Type of image must be None, jpg or png")
        if path is None or path == "":
            raise ValueError("No path specified")
        elif type(path) is not str:
            raise ValueError("Path must be a string")
        else:
            self.input_path = path
            self.type_of_image = type_of_image

    def specify_output_path(self, path):
        """
        If you want to save the augmented images to a specific path, you can specify that path here.
        If this is not specified, the augmented images will be saved to the same path as the original images in an augmented folder.

        Parameters
        ----------
        path : str
            The path to the folder where the augmented images will be saved.

        Raises
        ------
        ValueError
            If the path is not a string.
            If the path is not specified.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.specify_output_path("/home/user/augmented-data/")
        Specifying that the augmented images will be stored at: /home/user/augmented-data/
        """
        if path is None or path == "":
            raise ValueError("No path specified")
        elif type(path) is not str:
            raise ValueError("Path must be a string")
        else:
            self.output_path = path

    # Functions that makes image clearer or blurrier.
    def do_gaussianBlur(self, intensity_from=0.5, intensity_to=3.0):
        """
        Applies gaussian blur to an image. It augments with a random intensity between the specified parameters.

        Parameters
        ----------
        intensity_from : float
            The lowest intensity of the gaussian blur. Ranging from 0 to unlimited. Intensity 0 is no blur. Intensity 3.0 is much blur.
        intensity_to : float
            The highest intensity of the gaussian blur. Ranging from 0 to unlimited.  Intensity 0 is no blur. Intensity 3.0 is much blur.

        Raises
        ------
        ValueError
            If the intensity_from or intensity_to is not a float or int.
            If the intensity_from is greater than the intensity_to.
            If the intensity_from or intensity_to is less than 0.0.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_gaussianBlur(0.5, 3.0)
        Adding gaussian blur to the augmenting todo list.
        This will gaussian blur an image with a random intensity between 0.5 and 3.0.

        """
        augmenting = augmenting_types.gaussianBlur(intensity_from, intensity_to)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Gaussian Blur")

    def do_sharpen(self, intensity_from=0.1, intensity_to=0.5):
        """
        Applies sharpen to an image. It augments with a random intensity between the specified parameters.

        Parameters
        ----------
        intensity_from : float
            The lowest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). Intensity 0 is no sharpen. Intensity 0.7 is much sharpen.
        intensity_to : float
            The highest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). Intensity 0 is no sharpen. Intensity 0.7 is much sharpen.

        Raises
        ------
        ValueError
            If the intensity_from or intensity_to is not a float or int.
            If the intensity_from is greater than the intensity_to.
            If the intensity_from or intensity_to less than 0.0.
            If the intensity_from or intensity_to is greater than 1.0.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_sharpen(0.1, 0.5)
        Adding sharpen to the augmenting todo list.
        This will sharpen an image with a random intensity between 0.1 and 0.5.
        """
        augmenting = augmenting_types.sharpen(intensity_from, intensity_to)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Sharpen")

    def do_saltAndPepper(self, intensity_from=0.1, intensity_to=0.5):
        """
        Adds salt and pepper noise to an image. It augments with a random intensity between the specified parameters.

        Parameters
        ----------
        intensity_from : float
            The lowest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). Intensity 0 is no noise. Intensity 0.7 is much noise.
        intensity_to : float
            The highest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). Intensity 0 is no noise. Intensity 0.7 is much noise.

        Raises
        ------
        ValueError
            If the intensity_from or intensity_to is not a float or int.
            If the intensity_from is greater than the intensity_to.
            If the intensity_from or intensity_to less than 0.0.
            If the intensity_from or intensity_to is greater than 1.0.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_saltAndPepper(0.1, 0.5)
        Adding salt and pepper noise to the augmenting todo list.
        This will add salt and pepper noise to an image with a random intensity between 0.1 and 0.5.

        """
        augmenting = augmenting_types.saltAndPepper(intensity_from, intensity_to)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Salt and Pepper")

    def do_additiveGaussianNoise(self, intensity_from=5, intensity_to=50):
        """
        Adds additive gaussian noise to an image. It augments with a random intensity between the specified parameters.

        Parameters
        ----------
        intensity_from : float
            The lowest percent of the additive guassian noise. Ranging from 0 to unlimited. Intensity 0 is no noise. Intensity 50 is much noise.
        intensity_to : float
            The highest percent of the additive guassian noise. Ranging from 0 to unlimited. Intensity 0 is no noise. Intensity 50 is much noise.

        Raises
        ------
        ValueError
            If the intensity_from or intensity_to is not a float or int.
            If the intensity_from is greater than the intensity_to.
            If the intensity_from or intensity_to less than 0.0.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_additiveGaussianNoise(5, 50)
        Adding additive guassian noise to the augmenting todo list.
        This will add gaussian noise to an image with a random intensity between 5 and 50.
        """
        augmenting = augmenting_types.additiveGuassianNoise(intensity_from, intensity_to)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Additive Gaussian Noise")

    # Functions that changes the position of the image.
    def do_rotate(self, rotation_left=180, rotation_right=180):
        """
        Rotates an image. It augments with a random rotation between the specified parameters.

        Parameters
        ----------
        rotation_left : int
            The amount of maximum rotation to the left. Ranging from 0 to 180. rotation_left=0 is no rotation to the left. rotation_left=180 is maximum 180 degrees rotation to the left.
        rotation_right : int
            The amount of maximum rotation to the right. Ranging from 0 to 180. rotation_right=0 is no rotation to the right. rotation_right=180 is maximum 180 degrees rotation to the right.

        Raises
        ------
        ValueError
            If the rotation_left or rotation_right is not an int or float.
            If the rotation_left or rotation_right is less than 0.
            If the rotation_left or rotation_right is greater than 180.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_rotate(90, 90)
        Adding rotation to the augmenting todo list.
        This will rotate an image a random amount of maximum 90 degrees to the left or maximum 90 degrees to the right.
        """
        augmenting = augmenting_types.rotation(rotation_left, rotation_right)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Rotate")

    def do_pad(self, left=20, right=20, top=20, bottom=20):
        """
        Pads an image. It augments with a random amount of padding between the specified parameters.

        Parameters
        ----------
        left : int
            The amount of padding to the left. Ranging from 0 to unlimited. left=0 is no padding on the left. left=20 is 20 pixels of padding on the left.
        right : int
            The amount of padding to the right. Ranging from 0 to unlimited. right=0 is no padding on the right. right=20 is 20 pixels of padding on the right.
        top : int
            The amount of padding to the top. Ranging from 0 to unlimited. top=0 is no padding on the top. top=20 is 20 pixels of padding on the top.
        bottom : int
            The amount of padding to the bottom. Ranging from 0 to unlimited. bottom=0 is no padding on the bottom. bottom=20 is 20 pixels of padding on the bottom.

        Raises
        ------
        ValueError
            If the left/right/top/bottom is not an int or float.
            If the left/right/top/bottom is less than 0.
            If left, right, top and bottom is all 0.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_pad(0, 5, 0, 20)
        Adding padding to the augmenting todo list.
        This will pad an image with a random amount of padding up to maximum 5px on the right, maximum 20px to the bottom and do no padding on the left and top.

        """
        augmenting = augmenting_types.pad(left, right, top, bottom)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Pad")

    def do_scale(self, zoom_out=0.5, zoom_in=1.5):
        """
        Scales an image. It augments with a random scale between the specified parameters.

        Parameters
        ----------
        zoom_out : float
            The amount of maximum zoom out. Ranging from 0.0 to unlimited. zoom_out=1.0 is no zoom out. zoom_out=0.5 is much zoom out.
        zoom_in : float
            The amount of maximum zoom in. Ranging from 0.0 to unlimited. zoom_in=1.0 is no zoom in. zoom_in=2.5 is much zoom in.

        Raises
        ------
        ValueError
            If the zoom_out or zoom_in is not an int or float.
            If the zoom_out is less than 0.
            If the zoom_in is less than 1.
            If the zoom_out is greater than zoom_in.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_scale(0.5, 1.5)
        Adding scaling to the augmenting todo list.
        This will scale an image a random amount of maximum 0.5 times out to maximum 1.5 times in.
        """
        augmenting = augmenting_types.scale(zoom_out, zoom_in)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Scale")


    # Combined functions
    def do_gaussianBlur_and_rotate(self, gaussianBlur_intensity_from=0.5, gaussianBlur_intensity_to=3.0, rotate_rotation_left=180, rotate_rotation_right=180):
        """
        Applies gaussian blur and rotation to an image. It augments with a random amount of guassian blur and rotation between the specified parameters.

        Parameters
        ----------
        gaussianBlur_intensity_from : float
            The lowest intensity of the gaussian blur. Ranging from 0 to unlimited. Intensity 0 is no blur. Intensity 3.0 is much blur.
        gaussianBlur_intensity_to : float
            The highest intensity of the gaussian blur. Ranging from 0 to unlimited.  Intensity 0 is no blur. Intensity 3.0 is much blur.
        rotate_rotation_left : int
            The amount of maximum rotation to the left. Ranging from 0 to 180. rotate_rotation_left=0 is no rotation to the left. rotate_rotation_left=180 is maximum 180 degrees rotation to the left.
        rotate_rotation_right : int
            The amount of maximum rotation to the right. Ranging from 0 to 180. rotate_rotation_right=0 is no rotation to the right. rotate_rotation_right=180 is maximum 180 degrees rotation to the right.


        Raises
        ------
        ValueError
            If the gaussianBlur_intensity_from or gaussianBlur_intensity_to is not a float or int.
            If the gaussianBlur_intensity_from is greater than the gaussianBlur_intensity_to.
            If the gaussianBlur_intensity_from or gaussianBlur_intensity_to is less than 0.0.
            If the rotate_rotation_left or rotation_right is not an int or float.
            If the rotate_rotation_left or rotate_rotation_right is less than 0.
            If the rotate_rotation_left or rotate_rotation_right is greater than 180.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_gaussianBlur_and_rotate(0.5, 3.0, 90, 90)
        Adding guassian blur and rotation to the augmenting todo list.
        This will gaussian blur an image with a random intensity between 0.5 and 3.0.
        And on the same image rotate the image a random amount of maximum 90 degrees to the left or maximum 90 degrees to the right
        """
        augmenting = augmenting_types.guassianBlur_and_rotate(gaussianBlur_intensity_from, gaussianBlur_intensity_to, rotate_rotation_left, rotate_rotation_right)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Gaussian Blur and Rotate")

    def do_gaussianBlur_and_pad(self, gaussianBlur_intensity_from=0.5, gaussianBlur_intensity_to=3.0, pad_left=20, pad_right=20, pad_top=20, pad_bottom=20):
        """
        Applies gaussian blur and padding to an image. It augments with a random amount of guassian blur and padding between the specified parameters.

        Parameters
        ----------
        gaussianBlur_intensity_from : float
            The lowest intensity of the gaussian blur. Ranging from 0 to unlimited. Intensity 0 is no blur. Intensity 3.0 is much blur.
        gaussianBlur_intensity_to : float
            The highest intensity of the gaussian blur. Ranging from 0 to unlimited.  Intensity 0 is no blur. Intensity 3.0 is much blur.
        pad_left : int
            The amount of padding to the left. Ranging from 0 to unlimited. pad_left=0 is no padding on the left. pad_left=20 is 20 pixels of padding on the left.
        pad_right : int
            The amount of padding to the right. Ranging from 0 to unlimited. pad_right=0 is no padding on the right. pad_right=20 is 20 pixels of padding on the right.
        pad_top : int
            The amount of padding to the top. Ranging from 0 to unlimited. pad_top=0 is no padding on the top. pad_top=20 is 20 pixels of padding on the top.
        pad_bottom : int
            The amount of padding to the bottom. Ranging from 0 to unlimited. pad_bottom=0 is no padding on the bottom. pad_bottom=20 is 20 pixels of padding on the bottom.

        Raises
        ------
        ValueError
            If the gaussianBlur_intensity_from or gaussianBlur_intensity_to is not a float or int.
            If the gaussianBlur_intensity_from is greater than the gaussianBlur_intensity_to.
            If the gaussianBlur_intensity_from or gaussianBlur_intensity_to is less than 0.0.
            If the pad_left/pad_right/pad_top/pad_bottom is not an int or float.
            If the pad_left/pad_right/pad_top/pad_bottom is less than 0.
            If pad_left, pad_right, pad_top and pad_bottom is all 0.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_gaussianBlur_and_pad(0.5, 3.0, 0, 5, 0, 20)
        Adding gaussian blur and padding to the augmenting todo list.
        This will guassian blur an image with a random intensity between 0.5 and 3.0.
        And pad the same image with a random amount of maximum 5px on the right, maximum 20px to the bottom and do no padding on the left and top.
        """

        augmenting = augmenting_types.guassianBlur_and_pad(gaussianBlur_intensity_from, gaussianBlur_intensity_to, pad_left, pad_right, pad_top, pad_bottom)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Gaussian Blur and Pad")

    def do_gaussianBlur_and_scale(self, gaussianBlur_intensity_from=0.5, gaussianBlur_intensity_to=3.0, scale_zoom_out=0.5, scale_zoom_in=1.5):
        """
        Applies gaussian blur and scaling to an image. It augments with a random amount of guassian blur and scaling between the specified parameters.

        Parameters
        ----------
        gaussianBlur_intensity_from : float
            The lowest intensity of the gaussian blur. Ranging from 0 to unlimited. Intensity 0 is no blur. Intensity 3.0 is much blur.
        gaussianBlur_intensity_to : float
            The highest intensity of the gaussian blur. Ranging from 0 to unlimited.  Intensity 0 is no blur. Intensity 3.0 is much blur.
        scale_zoom_out : float
            The amount of maximum zoom out. Ranging from 0.0 to unlimited. scale_zoom_out=1.0 is no zoom out. scale_zoom_out=0.5 is much zoom out.
        scale_zoom_in : float
            The amount of maximum zoom in. Ranging from 0.0 to unlimited. scale_zoom_in=1.0 is no zoom in. scale_zoom_in=2.5 is much zoom in.

        Raises
        ------
        ValueError
            If the gaussianBlur_intensity_from or gaussianBlur_intensity_to is not a float or int.
            If the gaussianBlur_intensity_from is greater than the gaussianBlur_intensity_to.
            If the gaussianBlur_intensity_from or gaussianBlur_intensity_to is less than 0.0.
            If the scale_zoom_out or scale_zoom_in is not an int or float.
            If the scale_zoom_out is less than 0.
            If the scale_zoom_in is less than 1.
            If the scale_zoom_out is greater than scale_zoom_in.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_gaussianBlur_and_scale(0.5, 3.0, 0.5, 1.5)
        Adding gaussian blur and scaling to the augmenting todo list.
        This will guassian blur an image with a random intensity between 0.5 and 3.0.
        And on the same image scales it a random amount of maximum 0.5 times out to maximum 1.5 times in.
        """

        augmenting = augmenting_types.guassianBlur_and_scale(gaussianBlur_intensity_from, gaussianBlur_intensity_to, scale_zoom_out, scale_zoom_in)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Gaussian Blur and Scale")

    def do_rotate_and_scale(self, rotate_rotation_left=180, rotate_rotation_right=180, scale_zoom_out=0.5, scale_zoom_in=1.5):
        """
        Applies rotation and scaling to an image. It augments with a random amount of rotation and scaling between the specified parameters.

        Parameters
        ----------
        rotate_rotation_left : int
            The amount of maximum rotation to the left. Ranging from 0 to 180. rotate_rotation_left=0 is no rotation to the left. rotate_rotation_left=180 is maximum 180 degrees rotation to the left.
        rotate_rotation_right : int
            The amount of maximum rotation to the right. Ranging from 0 to 180. rotate_rotation_right=0 is no rotation to the right. rotate_rotation_right=180 is maximum 180 degrees rotation to the right.
        scale_zoom_out : float
            The amount of maximum zoom out. Ranging from 0.0 to unlimited. scale_zoom_out=1.0 is no zoom out. scale_zoom_out=0.5 is much zoom out.
        scale_zoom_in : float
            The amount of maximum zoom in. Ranging from 0.0 to unlimited. scale_zoom_in=1.0 is no zoom in. scale_zoom_in=2.5 is much zoom in.

        Raises
        ------
        ValueError
            If the rotate_rotation_left or rotate_rotation_right is not a float or int.
            If the rotate_rotation_left or rotate_rotation_right is less than 0.0.
            If the scale_zoom_out or scale_zoom_in is not an int or float.
            If the scale_zoom_out is less than 0.
            If the scale_zoom_in is less than 1.
            If the scale_zoom_out is greater than scale_zoom_in.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_rotate_and_scale(90, 90, 0.5, 1.5)
        Adding rotation and scaling to the augmenting todo list.
        This will rotate an image a random amount of maximum 90 degrees to the left or right.
        And on the same image scales it a random amount of maximum 0.5 times out to maximum 1.5 times in.
        """
        augmenting = augmenting_types.rotate_and_scale(rotate_rotation_left, rotate_rotation_right, scale_zoom_out, scale_zoom_in)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Rotate and Scale")

    def do_sharpen_and_rotate(self, sharpen_intensity_from=0.1, sharpen_intensity_to=0.5, rotate_rotation_left=180, rotate_rotation_right=180):
        """
        Applies sharpen and rotation to an image. It augments with a random amount of sharpen and rotation between the specified parameters.

        Parameters
        ----------
        sharpen_intensity_from : float
            The lowest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). Sharpen_intensity 0 is no sharpen. Sharpen_intensity 0.7 is much sharpen.
        sharpen_intensity_to : float
            The highest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). Sharpen_intensity 0 is no sharpen. Sharpen_intensity 0.7 is much sharpen.
        rotate_rotation_left : int
            The amount of maximum rotation to the left. Ranging from 0 to 180. rotate_rotation_left=0 is no rotation to the left. rotate_rotation_left=180 is maximum 180 degrees rotation to the left.
        rotate_rotation_right : int
            The amount of maximum rotation to the right. Ranging from 0 to 180. rotate_rotation_right=0 is no rotation to the right. rotate_rotation_right=180 is maximum 180 degrees rotation to the right.

        Raises
        ------
        ValueError
            If the sharpen_intensity_from or sharpen_intensity_to is not a float or int.
            If the sharpen_intensity_from is greater than the sharpen_intensity_to.
            If the sharpen_intensity_from or sharpen_intensity_to less than 0.0.
            If the sharpen_intensity_from or sharpen_intensity_to is greater than 1.0.
            If the rotate_rotation_left or rotate_rotation_right is not a float or int.
            If the rotate_rotation_left or rotate_rotation_right is less than 0.0.
            If the rotate_rotation_left or rotate_rotation_right is greater than 180.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_sharpen_and_rotate(0.1, 0.5, 90, 90)
        Adding sharpen and rotation to the augmenting todo list.
        This will sharpen an image with a random intensity between 0.1 and 0.5.
        And rotate the same image a random amount of maximum 90 degrees to the left or right.
        """

        augmenting = augmenting_types.sharpen_and_rotate(sharpen_intensity_from, sharpen_intensity_to, rotate_rotation_left, rotate_rotation_right)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Sharpen and Rotate")

    def do_sharpen_and_pad(self, sharpen_intensity_from=0.1, sharpen_intensity_to=0.5, pad_left=20, pad_right=20, pad_top=20, pad_bottom=20):
        """
        Applies sharpen and padding to an image. It augments with a random amount of sharpen and padding between the specified parameters.

        Parameters
        ----------
        sharpen_intensity_from : float
            The lowest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). Sharpen_intensity 0 is no sharpen. Sharpen_intensity 0.7 is much sharpen.
        sharpen_intensity_to : float
            The highest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). Sharpen_intensity 0 is no sharpen. Sharpen_intensity 0.7 is much sharpen.
        pad_left : int
            The amount of padding to the left. Ranging from 0 to unlimited. pad_left=0 is no padding on the left. pad_left=20 is 20 pixels of padding on the left.
        pad_right : int
            The amount of padding to the right. Ranging from 0 to unlimited. pad_right=0 is no padding on the right. pad_right=20 is 20 pixels of padding on the right.
        pad_top : int
            The amount of padding to the top. Ranging from 0 to unlimited. pad_top=0 is no padding on the top. pad_top=20 is 20 pixels of padding on the top.
        pad_bottom : int
            The amount of padding to the bottom. Ranging from 0 to unlimited. pad_bottom=0 is no padding on the bottom. pad_bottom=20 is 20 pixels of padding on the bottom.

        Raises
        ------
        ValueError
            If the sharpen_intensity_from or sharpen_intensity_to is not a float or int.
            If the sharpen_intensity_from is greater than the sharpen_intensity_to.
            If the sharpen_intensity_from or sharpen_intensity_to less than 0.0.
            If the sharpen_intensity_from or sharpen_intensity_to is greater than 1.0.
            If the pad_left/pad_right/pad_top/pad_bottom is not an int or float.
            If the pad_left/pad_right/pad_top/pad_bottom is less than 0.
            If pad_left, pad_right, pad_top and pad_bottom is all 0.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_sharpen_and_pad(0.1, 0.5, 0, 5, 0, 20)
        Adding sharpen and padding to the augmenting todo list.
        This will sharpen an image with a random intensity between 0.1 and 0.5.
        And on the same image pad with a random amount of padding up to maximum 5px on the right, maximum 20px to the bottom and do no padding on the left and top.
        And pad the same image with a random amount of maximum 5px on the right, maximum 20px to the bottom and do no padding on the left and top.
        """

        augmenting = augmenting_types.sharpen_and_pad(sharpen_intensity_from, sharpen_intensity_to, pad_left, pad_right, pad_top, pad_bottom)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Sharpen and Pad")

    def do_sharpen_and_scale(self, sharpen_intensity_from=0.1, sharpen_intensity_to=0.5, scale_zoom_out=0.5, scale_zoom_in=1.5):
        """
        Applies sharpen and scaling to an image. It augments with a random amount of sharpen and scaling between the specified parameters.

        Parameters
        ----------
        sharpen_intensity_from : float
            The lowest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). Sharpen_intensity 0 is no sharpen. Sharpen_intensity 0.7 is much sharpen.
        sharpen_intensity_to : float
            The highest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). Sharpen_intensity 0 is no sharpen. Sharpen_intensity 0.7 is much sharpen.
        scale_zoom_out : float
            The amount of maximum zoom out. Ranging from 0.0 to unlimited. scale_zoom_out=1.0 is no zoom out. scale_zoom_out=0.5 is much zoom out.
        scale_zoom_in : float
            The amount of maximum zoom in. Ranging from 0.0 to unlimited. scale_zoom_in=1.0 is no zoom in. scale_zoom_in=2.5 is much zoom in.

        Raises
        ------
        ValueError
            If the sharpen_intensity_from or sharpen_intensity_to is not a float or int.
            If the sharpen_intensity_from is greater than the sharpen_intensity_to.
            If the sharpen_intensity_from or sharpen_intensity_to less than 0.0.
            If the sharpen_intensity_from or sharpen_intensity_to is greater than 1.0.
            If the scale_zoom_out or scale_zoom_in is not an int or float.
            If the scale_zoom_out is less than 0.
            If the scale_zoom_in is less than 1.
            If the scale_zoom_out is greater than scale_zoom_in.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_sharpen_and_scale(0.1, 0.5, 0.5, 1.5)
        Adding sharpen and scaling to the augmenting todo list.
        This will sharpen an image with a random intensity between 0.1 and 0.5.
        And on the same image scales it a random amount of maximum 0.5 times out to maximum 1.5 times in.

        """
        augmenting = augmenting_types.sharpen_and_scale(sharpen_intensity_from, sharpen_intensity_to, scale_zoom_out, scale_zoom_in)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Sharpen and Scale")

    def do_saltAndPepper_and_rotate(self, saltAndPepper_intensity_from=0.1, saltAndPepper_intensity_to=0.5, rotate_rotation_left=180, rotate_rotation_right=180):
        """
        Applies salt and pepper noise and rotation to an image. It augments with a random amount of salt and pepper noise and rotation between the specified parameters.

        Parameters
        ----------
        saltAndPepper_intensity_from : float
            The lowest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). SaltAndPepper_intensity 0 is no noise. SaltAndPepper_intensity 0.7 is much noise.
        saltAndPepper_intensity_to : float
            The highest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). SaltAndPepper_intensity 0 is no noise. SaltAndPepper_intensity 0.7 is much noise.
        rotate_rotation_left : int
            The amount of maximum rotation to the left. Ranging from 0 to 180. rotate_rotation_left=0 is no rotation to the left. rotate_rotation_left=180 is maximum 180 degrees rotation to the left.
        rotate_rotation_right : int
            The amount of maximum rotation to the right. Ranging from 0 to 180. rotate_rotation_right=0 is no rotation to the right. rotate_rotation_right=180 is maximum 180 degrees rotation to the right.

        Raises
        ------
        ValueError
            If the saltAndPepper_intensity_from or saltAndPepper_intensity_to is not a float or int.
            If the saltAndPepper_intensity_from is greater than the saltAndPepper_intensity_to.
            If the saltAndPepper_intensity_from or saltAndPepper_intensity_to less than 0.0.
            If the saltAndPepper_intensity_from or saltAndPepper_intensity_to is greater than 1.0.
            If the rotate_rotation_left or rotate_rotation_right is not a float or int.
            If the rotate_rotation_left or rotate_rotation_right is less than 0.0.
            If the rotate_rotation_left or rotate_rotation_right is greater than 180.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_saltAndPepper_and_rotate(0.1, 0.5, 90, 90)
        Adding salt and pepper noise and rotation to the augmenting todo list.
        This will add salt and pepper noise to an image with a random intensity between 0.1 and 0.5.
        And rotate the same image a random amount of maximum 90 degrees to the left or right.
        """
        augmenting = augmenting_types.saltAndPepper_and_rotate(saltAndPepper_intensity_from, saltAndPepper_intensity_to, rotate_rotation_left, rotate_rotation_right)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Salt and Pepper and Rotate")

    def do_saltAndPepper_and_pad(self, saltAndPepper_intensity_from=0.1, saltAndPepper_intensity_to=0.5, pad_left=20, pad_right=20, pad_top=20, pad_bottom=20):
        """
        Applies salt and pepper noise and padding to an image. It augments with a random amount of salt and pepper noise and padding between the specified parameters.

        Parameters
        ----------
        saltAndPepper_intensity_from : float
            The lowest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). SaltAndPepper_intensity 0 is no noise. SaltAndPepper_intensity 0.7 is much noise.
        saltAndPepper_intensity_to : float
            The highest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). SaltAndPepper_intensity 0 is no noise. SaltAndPepper_intensity 0.7 is much noise.
        pad_left : int
            The amount of padding to the left. Ranging from 0 to unlimited. pad_left=0 is no padding on the left. pad_left=20 is 20 pixels of padding on the left.
        pad_right : int
            The amount of padding to the right. Ranging from 0 to unlimited. pad_right=0 is no padding on the right. pad_right=20 is 20 pixels of padding on the right.
        pad_top : int
            The amount of padding to the top. Ranging from 0 to unlimited. pad_top=0 is no padding on the top. pad_top=20 is 20 pixels of padding on the top.
        pad_bottom : int
            The amount of padding to the bottom. Ranging from 0 to unlimited. pad_bottom=0 is no padding on the bottom. pad_bottom=20 is 20 pixels of padding on the bottom.

        Raises
        ------
        ValueError
            If the saltAndPepper_intensity_from or saltAndPepper_intensity_to is not a float or int.
            If the saltAndPepper_intensity_from is greater than the saltAndPepper_intensity_to.
            If the saltAndPepper_intensity_from or saltAndPepper_intensity_to less than 0.0.
            If the saltAndPepper_intensity_from or saltAndPepper_intensity_to is greater than 1.0.
            If the pad_left/pad_right/pad_top/pad_bottom is not an int or float.
            If the pad_left/pad_right/pad_top/pad_bottom is less than 0.
            If pad_left, pad_right, pad_top and pad_bottom is all 0.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_saltAndPepper_and_pad(0.1, 0.5, 0, 5, 0, 20)
        Adding salt and pepper noise and padding to the augmenting todo list.
        This will add salt and pepper noise to an image with a random intensity between 0.1 and 0.5.
        And pad the same image with a random amount of maximum 5px on the right, maximum 20px to the bottom and do no padding on the left and top.
        """

        augmenting = augmenting_types.saltAndPepper_and_pad(saltAndPepper_intensity_from, saltAndPepper_intensity_to, pad_left, pad_right, pad_top, pad_bottom)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Salt and Pepper and Pad")

    def do_saltAndPepper_and_scale(self, saltAndPepper_intensity_from=0.1, saltAndPepper_intensity_to=0.5, scale_zoom_out=0.5, scale_zoom_in=1.5):
        """
        Applies salt and pepper noise and scaling to an image. It augments with a random amount of salt and pepper noise and scaling between the specified parameters.

        Parameters
        ----------
        saltAndPepper_intensity_from : float
            The lowest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). SaltAndPepper_intensity 0 is no noise. SaltAndPepper_intensity 0.7 is much noise.
        saltAndPepper_intensity_to : float
            The highest percent intensity of the sharpen. Ranging from 0.0 (0%) to 1.0 (100%). SaltAndPepper_intensity 0 is no noise. SaltAndPepper_intensity 0.7 is much noise.
        scale_zoom_out : float
            The amount of maximum zoom out. Ranging from 0.0 to unlimited. scale_zoom_out=1.0 is no zoom out. scale_zoom_out=0.5 is much zoom out.
        scale_zoom_in : float
            The amount of maximum zoom in. Ranging from 0.0 to unlimited. scale_zoom_in=1.0 is no zoom in. scale_zoom_in=2.5 is much zoom in.

        Raises
        ------
        ValueError
            If the saltAndPepper_intensity_from or saltAndPepper_intensity_to is not a float or int.
            If the saltAndPepper_intensity_from is greater than the saltAndPepper_intensity_to.
            If the saltAndPepper_intensity_from or saltAndPepper_intensity_to less than 0.0.
            If the saltAndPepper_intensity_from or saltAndPepper_intensity_to is greater than 1.0.
            If the scale_zoom_out or scale_zoom_in is not an int or float.
            If the scale_zoom_out is less than 0.
            If the scale_zoom_in is less than 1.
            If the scale_zoom_out is greater than scale_zoom_in.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_saltAndPepper_and_scale(0.1, 0.5, 0.5, 1.5)
        Adding salt and pepper noise and scaling to the augmenting todo list.
        This will add salt and pepper noise to an image with a random intensity between 0.1 and 0.5.
        And on the same image scales it a random amount of maximum 0.5 times out to maximum 1.5 times in.
        """
        augmenting = augmenting_types.saltAndPepper_and_scale(saltAndPepper_intensity_from, saltAndPepper_intensity_to, scale_zoom_out, scale_zoom_in)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Salt and Pepper and Scale")

    def do_additiveGuassianNoise_and_rotate(self, additiveGuassianNoise_intensity_from=5, additiveGuassianNoise_intensity_to=50, rotate_rotation_left=180, rotate_rotation_right=180):
        """
        Applies additive guassian noise and rotation to an image. It augments with a random amount of additive guassian noise and rotation between the specified parameters.

        Parameters
        ----------
        additiveGuassianNoise_intensity_from : float
            The lowest percent of the additive guassian noise. Ranging from 0 to unlimited. AdditiveGuassianNoise_intensity 0 is no noise. AdditiveGuassianNoise_intensity 50 is much noise.
        additiveGuassianNoise_intensity_to : float
            The highest percent of the additive guassian noise. Ranging from 0 to unlimited. AdditiveGuassianNoise_intensity 0 is no noise. AdditiveGuassianNoise_intensity 50 is much noise.
        rotate_rotation_left : int
            The amount of maximum rotation to the left. Ranging from 0 to 180. rotate_rotation_left=0 is no rotation to the left. rotate_rotation_left=180 is maximum 180 degrees rotation to the left.
        rotate_rotation_right : int
            The amount of maximum rotation to the right. Ranging from 0 to 180. rotate_rotation_right=0 is no rotation to the right. rotate_rotation_right=180 is maximum 180 degrees rotation to the right.

        Raises
        ------
        ValueError
            If the additiveGuassianNoise_intensity_from or additiveGuassianNoise_intensity_to is not a float or int.
            If the additiveGuassianNoise_intensity_from is greater than the additiveGuassianNoise_intensity_to.
            If the additiveGuassianNoise_intensity_from or additiveGuassianNoise_intensity_to less than 0.0.
            If the rotate_rotation_left or rotate_rotation_right is not a float or int.
            If the rotate_rotation_left or rotate_rotation_right is less than 0.0.
            If the rotate_rotation_left or rotate_rotation_right is greater than 180.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_additiveGuassianNoise_and_rotate(5, 50, 90, 90)
        Adding additive guassian noise to the augmenting todo list.
        This will add guassian noise to an image with a random intensity between 5 and 50.
        And rotate the same image a random amount of maximum 90 degrees to the left or right.
        """
        augmenting = augmenting_types.additiveGuassianNoise_and_rotate(additiveGuassianNoise_intensity_from, additiveGuassianNoise_intensity_to, rotate_rotation_left, rotate_rotation_right)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Additive Guassian Noise and Rotate")

    def do_additiveGuassianNoise_and_pad(self, additiveGuassianNoise_intensity_from=5, additiveGuassianNoise_intensity_to=50, pad_left=20, pad_right=20, pad_top=20, pad_bottom=20):
        """
        Applies additive guassian noise and padding to an image. It augments with a random amount of additive guassian noise and padding between the specified parameters.

        Parameters
        ----------
        additiveGuassianNoise_intensity_from : float
            The lowest percent of the additive guassian noise. Ranging from 0 to unlimited. AdditiveGuassianNoise_intensity 0 is no noise. AdditiveGuassianNoise_intensity 50 is much noise.
        additiveGuassianNoise_intensity_to : float
            The highest percent of the additive guassian noise. Ranging from 0 to unlimited. AdditiveGuassianNoise_intensity 0 is no noise. AdditiveGuassianNoise_intensity 50 is much noise.
        pad_left : int
            The amount of padding to the left. Ranging from 0 to unlimited. pad_left=0 is no padding on the left. pad_left=20 is 20 pixels of padding on the left.
        pad_right : int
            The amount of padding to the right. Ranging from 0 to unlimited. pad_right=0 is no padding on the right. pad_right=20 is 20 pixels of padding on the right.
        pad_top : int
            The amount of padding to the top. Ranging from 0 to unlimited. pad_top=0 is no padding on the top. pad_top=20 is 20 pixels of padding on the top.
        pad_bottom : int
            The amount of padding to the bottom. Ranging from 0 to unlimited. pad_bottom=0 is no padding on the bottom. pad_bottom=20 is 20 pixels of padding on the bottom.

        Raises
        ------
        ValueError
            If the additiveGuassianNoise_intensity_from or additiveGuassianNoise_intensity_to is not a float or int.
            If the additiveGuassianNoise_intensity_from is greater than the additiveGuassianNoise_intensity_to.
            If the additiveGuassianNoise_intensity_from or additiveGuassianNoise_intensity_to less than 0.0.
            If the pad_left/pad_right/pad_top/pad_bottom is not an int or float.
            If the pad_left/pad_right/pad_top/pad_bottom is less than 0.
            If pad_left, pad_right, pad_top and pad_bottom is all 0.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_additiveGuassianNoise_and_pad(5, 50, 0, 5, 0, 20)
        Adding additive guassian noise and padding to the augmenting todo list.
        This will add guassian noise to an image with a random intensity between 5 and 50.
        And pad the same image with a random amount of maximum 5px on the right, maximum 20px to the bottom and do no padding on the left and top.
        """
        augmenting = augmenting_types.additiveGuassianNoise_and_pad(additiveGuassianNoise_intensity_from, additiveGuassianNoise_intensity_to, pad_left, pad_right, pad_top, pad_bottom)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Additive Guassian Noise and Pad")

    def do_additiveGuassianNoise_and_scale(self, additiveGuassianNoise_intensity_from=5, additiveGuassianNoise_intensity_to=50, scale_zoom_out=0.5, scale_zoom_in=1.5):
        """
        Applies additive guassian noise and scaling to an image. It augments with a random amount of additive guassian noise and scaling between the specified parameters.

        Parameters
        ----------
        additiveGuassianNoise_intensity_from : float
            The lowest percent of the additive guassian noise. Ranging from 0 to unlimited. AdditiveGuassianNoise_intensity 0 is no noise. AdditiveGuassianNoise_intensity 50 is much noise.
        additiveGuassianNoise_intensity_to : float
            The highest percent of the additive guassian noise. Ranging from 0 to unlimited. AdditiveGuassianNoise_intensity 0 is no noise. AdditiveGuassianNoise_intensity 50 is much noise.
        scale_zoom_out : float
            The amount of maximum zoom out. Ranging from 0.0 to unlimited. scale_zoom_out=1.0 is no zoom out. scale_zoom_out=0.5 is much zoom out.
        scale_zoom_in : float
            The amount of maximum zoom in. Ranging from 0.0 to unlimited. scale_zoom_in=1.0 is no zoom in. scale_zoom_in=2.5 is much zoom in.

        Raises
        ------
        ValueError
            If the additiveGuassianNoise_intensity_from or additiveGuassianNoise_intensity_to is not a float or int.
            If the additiveGuassianNoise_intensity_from is greater than the additiveGuassianNoise_intensity_to.
            If the additiveGuassianNoise_intensity_from or additiveGuassianNoise_intensity_to less than 0.0.
            If the scale_zoom_out or scale_zoom_in is not an int or float.
            If the scale_zoom_out is less than 0.
            If the scale_zoom_in is less than 1.
            If the scale_zoom_out is greater than scale_zoom_in.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.do_additiveGuassianNoise_and_scale(5, 50, 0.5, 1.5)
        Adding additive guassian noise and scaling to the augmenting todo list.
        This will add guassian noise to an image with a random intensity between 5 and 50.
        And on the same image scales it a random amount of maximum 0.5 times out to maximum 1.5 times in.
        """

        augmenting = augmenting_types.additiveGuassianNoise_and_scale(additiveGuassianNoise_intensity_from, additiveGuassianNoise_intensity_to, scale_zoom_out, scale_zoom_in)
        self.augmentation_todo.add(augmenting)
        self.todo_names.append("Additive Guassian Noise and Scale")


    # Testing the augmenation by visualising the images.
    def run_view(self):
        """
        A testing and visualising function.

        Augments 9 random images from the specified path. Augments using each of the augmentation types added to the todo list and visualises them in a 3x3 grid.
        This is to test1 the augmentation and to see how much each augmentation type affects the images.
        This function does not save the augmented images and can be a nice function to run before the actual augmentation of all the images.
        After this function is run a user can tweek the parameters of the augmentation types and test1 the augmentation on the images again. Then when satisfied run the augmentation.

        Raises
        ------
        ValueError
            If the path is not specified.
            If no augmentation types is added to the todo list.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.specify_input_path("/path/to/images")
        >>> augmenter.do_rotate(90, 90)
        >>> augmenter.do_additiveGuassianNoise_and_scale(5, 50, 0.5, 1.5)
        >>> augmenter.run_view()
        Augments 9 random images from the specified path and visualises them in a 3x3 grid for each augmenting type.
        Augments 9 images using the 'do_rotate' augmentation type.
        And augments 9 images using the 'do_additiveGuassianNoise_and_scale' augmentation type.
        Then visualises:
        1. The original images in a 3x3 grid.
        2. The augmented images using 'do_rotate' in a 3x3 grid.
        3. The augmented images using 'do_additiveGuassianNoise_and_scale' in a 3x3 grid.
        """

        # Raises ValueError if something is wrong.
        if self.input_path is None:
            raise ValueError("No path specified")
        elif len(self.augmentation_todo) == 0:
            raise ValueError("No augmentation specified")
        else:
            run_view.view_augment(self.input_path, self.type_of_image, self.augmentation_todo, self.todo_names)

    def stats(self):
        pass

    # Augmenting the images.
    def run_augment(self):
        """
        Augments the images in the specified path. It will create new folders containing the augmented images following the structure of the rootfolder and subfolder of the specified path.
        In mypath/user/home path the home is root folder. All folders under home/.. is subfolders.
        If the output_path is specified the augmented images will be saved to the output_path instead.
        Keep in mind that if this is run multiple times at the same specified path it will replace the old folders images.

        Parameters
        ----------

        Raises
        ------
        ValueError
            If the path is not specified.
            If no augmentation types is added to the todo list.

        Returns
        -------

        Examples
        --------
        >>> from easyaug.augment import Augmenter
        >>> augmenter = Augmenter()
        >>> augmenter.specify_input_path("/path/to/data/folder")
        >>> augmenter.do_rotate(90, 90)
        >>> augmenter.do_additiveGuassianNoise_and_scale(5, 50, 0.5, 1.5)
        >>> augmenter.run_augment()
        Augments the images in the specified path. It will create new folders containing the augmented images following the structure of the rootfolder and subfolder of the specified path.
        This will augment using the 'do_rotate' and 'do_additiveGuassianNoise_and_scale' augmentation types.
        """

        if self.input_path is None:
            raise ValueError("No input path specified")
        elif len(self.augmentation_todo) == 0:
            raise ValueError("No augmentation specified")
        else:
            run_augment.augment(self.input_path, self.output_path, self.type_of_image, self.augmentation_todo, self.todo_names)

