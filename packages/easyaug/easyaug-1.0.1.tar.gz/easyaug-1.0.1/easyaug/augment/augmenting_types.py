from imgaug import augmenters as iaa

# Functions that makes image clearer or blurrier.
def gaussianBlur(intensity_from, intensity_to):
    # If intensity_from is int then make it a float.
    if isinstance(intensity_from, int):
        intensity_from = float(intensity_from)
    # If intensity_to is int then make it a float.
    if isinstance(intensity_to, int):
        intensity_to = float(intensity_to)

    # If insensity_from/to is not a float then raise an error.
    if not isinstance(intensity_from, float) or not isinstance(intensity_to, float):
        raise ValueError("intensity_from and intensity_to must be floats.")

    # If intensity_from is larger than intensity_to then raise an error.
    if intensity_from > intensity_to:
        raise ValueError("intensity_from must be less than intensity_to.")

    # If intensity_from is less than 0 then raise an error.
    if intensity_from < 0:
        raise ValueError("intensity_from must be greater than 0.")

    # Creating the guassian blur augmentation
    augmenting = iaa.GaussianBlur(sigma=(intensity_from, intensity_to))
    return augmenting

def sharpen(intensity_from, intensity_to):
    # If intensity_from is int then make it a float.
    if isinstance(intensity_from, int):
        intensity_from = float(intensity_from)
    # If intensity_to is int then make it a float.
    if isinstance(intensity_to, int):
        intensity_to = float(intensity_to)

    # If insensity_from/to is not a float then raise an error.
    if not isinstance(intensity_from, float) or not isinstance(intensity_to, float):
        raise ValueError("intensity_from and intensity_to must be floats.")

    # If intensity_from is larger than intensity_to then raise an error.
    if intensity_from > intensity_to:
        raise ValueError("intensity_from must be less than intensity_to.")

    # If intensity_from is less than 0 then raise an error.
    if intensity_from < 0:
        raise ValueError("intensity_from must be greater than 0.")
    # If intensity_to is more than 1 then raise an error.
    if intensity_to > 1:
        raise ValueError("intensity_to must be less than 1.")

    # Creating the sharpen augmentation
    augmenting = iaa.Sharpen(intensity_from, intensity_to)
    return augmenting

def saltAndPepper(intensity_from, intensity_to):
    # If intensity_from is int then make it a float.
    if isinstance(intensity_from, int):
        intensity_from = float(intensity_from)
    # If intensity_to is int then make it a float.
    if isinstance(intensity_to, int):
        intensity_to = float(intensity_to)

    # If insensity_from/to is not a float then raise an error.
    if not isinstance(intensity_from, float) or not isinstance(intensity_to, float):
        raise ValueError("intensity_from and intensity_to must be floats.")

    # If intensity_from is larger than intensity_to then raise an error.
    if intensity_from > intensity_to:
        raise ValueError("intensity_from must be less than intensity_to.")

    # If intensity_from is less than 0 then raise an error.
    if intensity_from < 0:
        raise ValueError("intensity_from must be greater than 0.")
    # If intensity_to is more than 1 then raise an error.
    if intensity_to > 1:
        raise ValueError("intensity_to must be less than 1.")

    # Creating the salt and pepper augmentation
    augmenting = iaa.SaltAndPepper((intensity_from, intensity_to))
    return augmenting

def additiveGuassianNoise(intensity_from, intensity_to):
    # If intensity_from is float then make it a float.
    if isinstance(intensity_from, float):
        intensity_from = float(intensity_from)
    # If intensity_to is float then make it a float.
    if isinstance(intensity_to, float):
        intensity_to = float(intensity_to)

    # If insensity_from/to is not a float then raise an error.
    if not isinstance(intensity_from, int) or not isinstance(intensity_to, int):
        raise ValueError("intensity_from and intensity_to must be ints.")

    # If intensity_from is larger than intensity_to then raise an error.
    if intensity_from > intensity_to:
        raise ValueError("intensity_from must be less than intensity_to.")

    # If intensity_from is less than 0 then raise an error.
    if intensity_from < 0:
        raise ValueError("intensity_from must be greater than 0.")

    # Creating the additive guassian noise augmentation
    augmenting = iaa.AdditiveGaussianNoise(scale=(intensity_from, intensity_to))
    return augmenting

# Functions that changes the position of the image.
def rotation(rotation_left, rotation_right):
    # If rotation_from/to is an integer then make it a float
    if isinstance(rotation_left, int):
        rotation_left = float(rotation_left)
    if isinstance(rotation_right, int):
        rotation_right = float(rotation_right)

    # Checking for parameter errors
    if rotation_left is None or rotation_right is None:
        raise ValueError("rotation_from and rotation_to cannot be None.")
    if not isinstance(rotation_left, float) or not isinstance(rotation_right, float):
        raise ValueError("rotation_from and rotation_to must be a float.")
    if rotation_left < 0 or rotation_right < 0:
        raise ValueError("rotation_from and rotation_to must be greater than 0.")
    if rotation_left > 180 or rotation_right > 180:
        raise ValueError("rotation_from and rotation_to must be less than 180.")

    # Creating the rotation augmentation
    augmenting = iaa.Rotate((-rotation_left, rotation_right))
    return augmenting

def pad(left, right, top, bottom):
    # If left/right/top/bottom is an float then make it an integer
    if isinstance(left, float):
        left = int(left)
    if isinstance(right, float):
        right = int(right)
    if isinstance(top, float):
        top = int(top)
    if isinstance(bottom, float):
        bottom = int(bottom)

    # Checking for parameter errors
    # If left/right/top/bottom is not and integer then raise an error
    if not isinstance(left, int) or not isinstance(right, int) or not isinstance(top, int) or not isinstance(bottom, int):
        raise ValueError("left, right, top, and bottom must be integers.")
    # If left/right/top/bottom is less than 0 then raise an error
    if left < 0 or right < 0 or top < 0 or bottom < 0:
        raise ValueError("left, right, top, and bottom must be greater than 0.")
    # If left/right/top/bottom is all 0 then raise an error
    if left < 0 and right == 0 and top == 0 and bottom == 0:
        raise ValueError("At least one of left, right, top, and bottom must be greater than 0.")


    left_default_minimum_pad = 5
    right_default_minimum_pad = 5
    top_default_minimum_pad = 5
    bottom_default_minimum_pad = 5
    # Changing default if parameters is lower than default.
    if left == 0:
        left_default_minimum_pad = 0
    elif left < 1:
        left_default_minimum_pad = left
    elif  left < left_default_minimum_pad:
        left_default_minimum_pad = 1
    if right == 0:
        right_default_minimum_pad = 0
    elif right < 1:
        right_default_minimum_pad = right
    elif right < right_default_minimum_pad:
        right_default_minimum_pad = 1
    if top == 0:
        top_default_minimum_pad = 0
    elif top < 1:
        top_default_minimum_pad = top
    elif top < top_default_minimum_pad:
        top_default_minimum_pad = 1
    if bottom == 0:
        bottom_default_minimum_pad = 0
    elif bottom < 1:
        bottom_default_minimum_pad = bottom
    elif bottom < bottom_default_minimum_pad:
        bottom_default_minimum_pad = 1


    # Creating Pad parameters from function parameters.
    left = (left_default_minimum_pad, left)
    right = (right_default_minimum_pad, right)
    top = (top_default_minimum_pad, top)
    bottom = (bottom_default_minimum_pad, bottom)

    # Creating the padding augmentation
    augmenting = iaa.Pad(px=(top, right, bottom, left))

    return augmenting

def scale(zoom_out, zoom_in):
    # If zoom_out is int then make it a float
    if isinstance(zoom_out, int):
        zoom_out = float(zoom_out)
    # If zoom_in is int then make it a float
    if isinstance(zoom_in, int):
        zoom_in = float(zoom_in)

    # Checking for parameter errors
    # If zoom_out/in is not a float then raise an error
    if not isinstance(zoom_out, float) or not isinstance(zoom_in, float):
        raise ValueError("zoom_out and zoom_in must be floats.")
    # If zoom_out/in is less than 0 then raise an error
    if zoom_out < 0:
        raise ValueError("zoom_out must be greater than 0.")
    if zoom_in < 1:
        raise ValueError("zoom_in must be greater than 1.")
    if zoom_out > zoom_in:
        raise ValueError("zoom_out must be less than zoom_in.")

    # Creating the scale augmentation
    augmenting = iaa.Affine(scale=(zoom_out, zoom_in))
    return augmenting


# Combined functions
def guassianBlur_and_rotate(guassianBlur_intensity_from, guassianBlur_intensity_to, rotate_rotation_left, rotate_rotation_right):
    sequential = iaa.Sequential()
    sequential.add(gaussianBlur(guassianBlur_intensity_from, guassianBlur_intensity_to))
    sequential.add(rotation(rotate_rotation_left, rotate_rotation_right))
    return sequential

def guassianBlur_and_scale(guassianBlur_intensity_from, guassianBlur_intensity_to, scale_zoom_out, scale_zoom_in):
    sequential = iaa.Sequential()
    sequential.add(gaussianBlur(guassianBlur_intensity_from, guassianBlur_intensity_to))
    sequential.add(scale(scale_zoom_out, scale_zoom_in))
    return sequential

def guassianBlur_and_pad(guassianBlur_intensity_from, guassianBlur_intensity_to, pad_left, pad_right, pad_top,
                         pad_bottom):
    sequential = iaa.Sequential()
    sequential.add(gaussianBlur(guassianBlur_intensity_from, guassianBlur_intensity_to))
    sequential.add(pad(pad_left, pad_right, pad_top, pad_bottom))
    return sequential

def rotate_and_scale(rotate_rotation_left, rotate_rotation_right, scale_zoom_out, scale_zoom_in):
    sequential = iaa.Sequential()
    sequential.add(rotation(rotate_rotation_left, rotate_rotation_right))
    sequential.add(scale(scale_zoom_out, scale_zoom_in))
    return sequential


def sharpen_and_rotate(sharpen_intensity_from, sharpen_intensity_to, rotate_rotation_left, rotate_rotation_right):
    sequential = iaa.Sequential()
    sequential.add(sharpen(sharpen_intensity_from, sharpen_intensity_to))
    sequential.add(rotation(rotate_rotation_left, rotate_rotation_right))
    return sequential

def sharpen_and_pad(sharpen_intensity_from, sharpen_intensity_to, pad_left, pad_right, pad_top, pad_bottom):
    sequential = iaa.Sequential()
    sequential.add(sharpen(sharpen_intensity_from, sharpen_intensity_to))
    sequential.add(pad(pad_left, pad_right, pad_top, pad_bottom))
    return sequential

def sharpen_and_scale(sharpen_intensity_from, sharpen_intensity_to, scale_zoom_out, scale_zoom_in):
    sequential = iaa.Sequential()
    sequential.add(sharpen(sharpen_intensity_from, sharpen_intensity_to))
    sequential.add(scale(scale_zoom_out, scale_zoom_in))
    return sequential


def saltAndPepper_and_rotate(saltAndPepper_intensity_from, saltAndPepper_intensity_to, rotate_rotation_left, rotate_rotation_right):
    sequential = iaa.Sequential()
    sequential.add(saltAndPepper(saltAndPepper_intensity_from, saltAndPepper_intensity_to))
    sequential.add(rotation(rotate_rotation_left, rotate_rotation_right))
    return sequential


def saltAndPepper_and_pad(saltAndPepper_intensity_from, saltAndPepper_intensity_to, pad_left, pad_right, pad_top, pad_bottom):
    sequential = iaa.Sequential()
    sequential.add(saltAndPepper(saltAndPepper_intensity_from, saltAndPepper_intensity_to))
    sequential.add(pad(pad_left, pad_right, pad_top, pad_bottom))
    return sequential


def saltAndPepper_and_scale(saltAndPepper_intensity_from, saltAndPepper_intensity_to, scale_zoom_out, scale_zoom_in):
    sequential = iaa.Sequential()
    sequential.add(saltAndPepper(saltAndPepper_intensity_from, saltAndPepper_intensity_to))
    sequential.add(scale(scale_zoom_out, scale_zoom_in))
    return sequential


def additiveGuassianNoise_and_rotate(additiveGuassianNoise_intensity_from, additiveGuassianNoise_intensity_to,
                                     rotate_rotation_left, rotate_rotation_right):
    sequential = iaa.Sequential()
    sequential.add(additiveGuassianNoise(additiveGuassianNoise_intensity_from, additiveGuassianNoise_intensity_to))
    sequential.add(rotation(rotate_rotation_left, rotate_rotation_right))
    return sequential


def additiveGuassianNoise_and_pad(additiveGuassianNoise_intensity_from, additiveGuassianNoise_intensity_to, pad_left,
                                  pad_right, pad_top, pad_bottom):
    sequential = iaa.Sequential()
    sequential.add(additiveGuassianNoise(additiveGuassianNoise_intensity_from, additiveGuassianNoise_intensity_to))
    sequential.add(pad(pad_left, pad_right, pad_top, pad_bottom))
    return sequential


def additiveGuassianNoise_and_scale(additiveGuassianNoise_intensity_from, additiveGuassianNoise_intensity_to,
                                    scale_zoom_out, scale_zoom_in):
    sequential = iaa.Sequential()
    sequential.add(additiveGuassianNoise(additiveGuassianNoise_intensity_from, additiveGuassianNoise_intensity_to))
    sequential.add(scale(scale_zoom_out, scale_zoom_in))
    return sequential