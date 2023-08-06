import glob
import os
import imageio
import shutil

class Folder:
    def __init__(self, folder_path, name_of_folder):
        self.folder_path = folder_path
        self.name_of_folder = name_of_folder
        self.list_of_folders = []
        self.list_of_images = []


def augment(path, output_path, type_of_image, augmentation_todo, todo_names):
    # If path does not end with a slash, add one.
    path = add_last_slash_if_needed(path)

    # Create a list of folders
    first_folder = Folder(path, name_of_folder(path))

    # Iterates through the first folder to find all images and folders
    iterate_folder(first_folder, type_of_image)

    # If the output path is None or empty, set the output path to the path of the first folder name+agumented.
    if output_path is None:
        # Creating the first augmented folder
        output_path = create_augment_folder(first_folder)
    else:
        # If the output path does not end with a slash, add one.
        output_path = add_last_slash_if_needed(output_path)
        # If the output path does not exist, create it.
        if not os.path.exists(output_path):
            os.mkdir(output_path)



    # Augments the images and creates new folders (called name_of_folder-augmented) with the augmented images.
    augment_images_or_iterate_folder(first_folder, output_path, augmentation_todo, todo_names)

def iterate_folder(folder, type_of_image):

    # Using glob finds all paths in the folder.folder_path
    for path in glob.glob(folder.folder_path + '*'):
        path = fix_slashes(path)
        # If a path is a folder, create a new folder object and add it to the list of folders.
        if os.path.isdir(path):
            path = add_last_slash_if_needed(path)
            new_folder = Folder(path, name_of_folder(path))
            folder.list_of_folders.append(new_folder)
            iterate_folder(new_folder, type_of_image)
        # If a path is an image and the type of image is not specified, add it to the list of images.
        elif os.path.isfile(path) and type_of_image is None:
            folder.list_of_images.append(path)
        # If a path is an image and the type of image is specified, add it to the list of images if it matches the type of image.
        elif os.path.isfile(path) and type_of_image is not None:
            if type_of_image == find_type_of_image(path):
                folder.list_of_images.append(path)


def create_augment_folder(folder, output_path=None):
    if output_path is not None:
        output_path = output_path + folder.name_of_folder
        output_path += '_augmented'
        output_path = add_last_slash_if_needed(output_path)
        # If the folder already exists, delete it then create a new one.
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        os.mkdir(output_path)
    else:
        output_path = folder.folder_path
        output_path = remove_last_slash(output_path)
        output_path += '_augmented'
        output_path = add_last_slash_if_needed(output_path)
        print(output_path)
        # If the folder already exists, delete it then create a new one.
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        os.mkdir(output_path)
    return output_path

def augment_images_or_iterate_folder(folder, output_path, augmentation_todo, todo_names):
    """Augment the images in the folder and iterates through the folders (if any) doing this recursive."""
    for image_path in folder.list_of_images:
        augment_image_and_write(image_path, output_path, augmentation_todo, todo_names)
    for subfolder in folder.list_of_folders:
        augment_images_or_iterate_folder(subfolder, create_augment_folder(subfolder, output_path), augmentation_todo, todo_names)


def augment_image_and_write(image_path, output_path, augmentation_todo, todo_names):
    """Augment the image in the image_path and save it to the output_path."""
    # Reads the image.
    image = imageio.imread(image_path)
    # Writes the image to the output_path.
    image_name = output_path + image_path.split('/')[-1]
    print('Augmenting image: ' + image_name)
    imageio.imwrite(image_name, image)

    # Finds what type image it is.
    type_of_image = find_type_of_image(image_path)

    # Augments the image.
    for augmentation, augmentation_name in zip(augmentation_todo, todo_names):
        augmented_image = augmentation(image=image)
        # If augmentation_name has spaces, replace them with underscores.
        if ' ' in augmentation_name:
            augmentation_name = augmentation_name.replace(' ', '_')
        # If the type of image is not specified, save the image as a jpg.
        # Saves the augmented image with the augmentation name.
        imageio.imwrite(output_path + image_path.split('/')[-1].split('.')[0] + '_' + augmentation_name + '.'+type_of_image, augmented_image)


def add_last_slash_if_needed(path):
    """Fix the path so that it ends with a slash."""
    if path[-1] != '/':
        path += '/'
    return path

def name_of_folder(path):
    """Return the name of the folder in the path."""
    return path.split('/')[-2]


def find_type_of_image(path):
    """Return the type of image in the path."""
    return path.split('.')[-1]


def remove_last_slash(path):
    """Remove the last slash in the path."""
    if path[-1] == '/':
        path = path[:-1]
    return path


def create_folder(output_path):
    """Delete the folder and all of its contents """
    shutil.rmtree(output_path)


def fix_slashes(path):
    """Fix the slashes in the path."""
    path = path.replace('\\', '/')
    return path


def read_image(image_path):
    """Read the image in the image_path."""
    image = imageio.imread(image_path)
    return image






