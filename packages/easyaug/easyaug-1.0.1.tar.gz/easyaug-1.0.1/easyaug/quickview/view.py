import matplotlib.pyplot as plt

def view_images(images, maximum):
    # Changing the maximum if its larger than the amount of images.
    if maximum > len(images):
        maximum = len(images)

    # Plotting images until maximum or amount of images is reached.
    # It will plot 9 images at a time until there will be less than 9 left before maximum or amount of images.
    # Then plot what is left.
    for index in range(0, maximum, 9):
        if index + 9 > maximum:
            pyplot_9_images(images[index:maximum])
            break
        pyplot_9_images(images[index:index+9])

    print("Visualized", maximum, "images from a total of", len(images), "possible.")


# Creating a pyplot containing at maximum 9 images.
def pyplot_9_images(images_max_9):
    # Predefined values.
    columns = 3 # If columns or rows is changed more code needs to be changes.
    rows = 3
    height_of_pyplot = 10
    width_of_pyplot = 10

    # Plotting.
    fig = plt.figure(figsize=(width_of_pyplot, height_of_pyplot))
    for i in range(0, len(images_max_9)):
        # Preparing plot for image.
        fig.add_subplot(rows, columns, i + 1)
        # Plotting image in preparet plot.
        plt.imshow(images_max_9[i])
        plt.axis("off")
        plt.title(get_name(images_max_9[i]._name))
    fig.tight_layout()
    plt.show()


def get_name(image_path):
    image_path_split = image_path.split("\\")
    imagename_dot_something = image_path_split[-1].split(".")
    imagename = imagename_dot_something[0]
    return imagename


def view_imagesnames(imagenames, maximum):
    if maximum > len(imagenames):
        maximum = len(imagenames)

    for index in range(0, maximum):
        print(get_name(imagenames[index]))

    print("Printed", maximum, "imagenames from a total of", len(imagenames), "possible.")


def view_imagesnames_from_images(images, maximum):
    if maximum > len(images):
        maximum = len(images)

    for index in range(0, maximum):
        print(get_name(images[index]._name))

    print("Printed", maximum, "imagenames from a total of", len(images), "possible.")