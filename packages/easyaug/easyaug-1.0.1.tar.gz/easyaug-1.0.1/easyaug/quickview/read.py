import glob
import os
import imageio


def read_all_images(path, type_of_image):
    # Getting all image names.
    imagenames = read_all_imagenames(path, type_of_image)

    # Checking if no images are found.
    no_images_error_handling(len(imagenames))

    # Getting all images by image names.
    images = []
    for imagename in imagenames:
        images.append(read_a_image(imagename))
    return images


def read_every_x_image(path, x, type_of_image):
    # Getting all image names.
    imagenames = read_all_imagenames(path, type_of_image)

    # Checking if no images are found.
    no_images_error_handling(len(imagenames))
    # Checking for errors on user input of x
    x_error_handling(x, len(imagenames))

    # Getting every x image
    images = []
    for index in range(0, len(imagenames), x):
        images.append(read_a_image(imagenames[index]))
    return images


def read_first_x_images(path, x, type_of_image):
    # Getting all image names.
    imagenames = read_all_imagenames(path, type_of_image)

    # Checking if no images are found.
    no_images_error_handling(len(imagenames))
    # Checking for errors on user input of x
    x_error_handling(x, len(imagenames))

    # Getting first x images.
    images = []
    for index in range(0, x):
        images.append(read_a_image(imagenames[index]))
    return images


def read_last_x_images(path, x, type_of_image):
    # Getting all image names.
    imagenames = read_all_imagenames(path, type_of_image)

    # Checking if no images are found.
    no_images_error_handling(len(imagenames))
    # Checking for errors on user input of x
    x_error_handling(x, len(imagenames))

    # Getting last x images.
    images = []
    for index in range(len(imagenames)-x, len(imagenames)):
        images.append(read_a_image(imagenames[index]))
    return images


def read_x_images(path, x, type_of_image):
    # Getting all image names.
    imagenames = read_all_imagenames(path, type_of_image)

    # Checking if no images are found.
    no_images_error_handling(len(imagenames))
    # Checking for errors on user input of x
    x_error_handling(x, len(imagenames))

    images = []
    if x == 0:
        index = int(len(imagenames) / 2)
        images.append(read_a_image(imagenames[index]))
    else:
        # Finding how much to step for each iteration to read x images.
        step = int((len(imagenames)+x)/x)

        # Getting 10 images with equal space inbetween.
        for index in range(0, len(imagenames), step):
            images.append(read_a_image(imagenames[index]))
    return images


def read_a_image(image_path):
    image = imageio.imread(image_path)
    image._name = image_path
    return image


def read_all_imagenames(path, type_of_image):
    # If path is not set with / it will add it.
    if path[-1] != "/":
        path = path+"/"

    # Find the images in this folder.
    imagenames = []
    if type_of_image is None:
        imagenames = glob.glob(path + "*")
    elif type_of_image == "jpg" or type_of_image == "png":
        imagenames = glob.glob(path + "*."+type_of_image)

    # If it finds a folder it will go into that and get those images too. Recursive.
    is_directories = []
    for image_name in imagenames:
        if os.path.isdir(image_name):
            is_directories.append(image_name)
            imagenames += read_all_imagenames(image_name, type_of_image)

    # Removes the directory paths.
    for is_directory in is_directories:
        imagenames.remove(is_directory)
    return imagenames

def no_images_error_handling(length_of_list):
    if length_of_list < 1:
        raise ValueError("No imagenames or images found.")


def x_error_handling(x, length_of_list=None):
    if length_of_list is not None:
        if not isinstance(x, int):
            raise ValueError("x must be an integer.")
        if x > length_of_list:
            raise ValueError("x cannot be larger than amount of images.")
        if x < 1:
            raise ValueError("x cannot be smaller than 1.")


def read_every_x_imagename(path, x, type_of_image):
    # Getting all image names.
    imagenames = read_all_imagenames(path, type_of_image)

    # Checking if no images are found.
    no_images_error_handling(len(imagenames))
    # Checking for errors on user input of x
    x_error_handling(x, len(imagenames))

    # Getting every x imagename
    imagenames_v2 = []
    for index in range(0, len(imagenames), x):
        imagenames_v2.append(imagenames[index])

    return imagenames_v2


def read_first_x_imagenames(path, x, type_of_image):
    # Getting all image names.
    imagenames = read_all_imagenames(path, type_of_image)

    # Checking if no images are found.
    no_images_error_handling(len(imagenames))
    # Checking for errors on user input of x
    x_error_handling(x, len(imagenames))

    # Getting first x imagenames.
    imagenames_v2 = []
    for index in range(0, x):
        imagenames_v2.append(imagenames[index])
    return imagenames_v2


def read_last_x_imagenames(path, x, type_of_image):
    # Getting all image names.
    imagenames = read_all_imagenames(path, type_of_image)

    # Checking if no images are found.
    no_images_error_handling(len(imagenames))
    # Checking for errors on user input of x
    x_error_handling(x, len(imagenames))

    # Getting last x imagenames.
    imagenames_v2 = []
    for index in range(len(imagenames) - x, len(imagenames)):
        imagenames_v2.append(imagenames[index])
    return imagenames_v2