import glob


def resize(input_path, output_path, type_of_image, size):
    """
    Resizes all images from path to output path
    """
    import os
    import cv2
    import numpy as np
    from PIL import Image
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # If inputpath does not end with /, add it
    if input_path[-1] != '/':
        input_path += '/'
    # If outputpath does not end with /, add it
    if output_path[-1] != '/':
        output_path += '/'

    # If type_of_image is specified, only resize images of that type

    # Using glob finds all images of type_of_image in path
    if type_of_image is not None:
        for image_path in glob.glob(input_path + '*.' + type_of_image):
            # Make all \ to /
            image_path = image_path.replace('\\', '/')
            # Loads image
            image = cv2.imread(image_path)
            # Resizes image
            image = cv2.resize(image, size)
            # Saves image
            cv2.imwrite(os.path.join(output_path, image_path.split('/')[-1]), image)
    # If type_of_image is not specified, resize all images
    else:
        for image_path in glob.glob(input_path + '*.*'):
            # Make all \ to /
            image_path = image_path.replace('\\', '/')
            # Loads image
            image = cv2.imread(image_path)
            # Resizes image
            image = cv2.resize(image, size)
            # Saves image
            path_to_save = (os.path.join(output_path, image_path.split('/')[-1]))
            print(path_to_save)
            cv2.imwrite(os.path.join(output_path, image_path.split('/')[-1]), image)








