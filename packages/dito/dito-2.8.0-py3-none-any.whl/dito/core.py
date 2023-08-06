import cv2
import numpy as np

import dito.utils


####
#%%% general
####


def is_image(image):
    """
    Return `True` iff the given image is either a valid grayscale image or a
    valid color image.
    """
    
    return is_gray(image=image) or is_color(image=image)


####
#%%% type-related
####


def is_integer_dtype(dtype):
    return np.issubdtype(dtype, np.integer)


def is_integer_image(image):
    return is_integer_dtype(dtype=image.dtype)


def is_float_dtype(dtype):
    return np.issubdtype(dtype, np.floating)


def is_float_image(image):
    return is_float_dtype(dtype=image.dtype)


def is_bool_dtype(dtype):
    return np.issubdtype(dtype, np.bool_)


def is_bool_image(image):
    return is_bool_dtype(dtype=image.dtype)


def dtype_range(dtype):
    """
    Returns the min and max intensity value of images for a given NumPy dtype.
    
    For integer dtypes, this corresponds to their full range.
    For floating dtypes, this corresponds to the range `(0.0, 1.0)`.
    For bool dtypes, this corresponds to the range (`False`, `True`).
    """
    if is_integer_dtype(dtype=dtype):
        info = np.iinfo(dtype)
        return (info.min, info.max)
    elif is_float_dtype(dtype=dtype):
        return (0.0, 1.0)
    elif is_bool_dtype(dtype=dtype):
        return (False, True)
    else:
        raise TypeError("Unsupported dtype '{}'".format(dtype))


def dtype_common(dtypes):
    """
    For a given vector `dtypes` of types, returns the type which supports
    all ranges.
    """

    hierarchy = (np.bool_, np.uint8, np.uint16, np.float32, np.float64)
    max_index = 0
    for dtype in dtypes:
        # check if `dtype` is a valid NumPy dtype
        try:
            np.dtype(dtype)
        except TypeError:
            raise ValueError("Invalid image type '{}'".format(dtype))

        # search for `dtype` in the hierarchy and update the max index if found
        for (index, value) in enumerate(hierarchy):
            if value == np.dtype(dtype):
                max_index = max(max_index, index)
                break
        else:
            raise ValueError("Invalid image type '{}'".format(dtype))
    return hierarchy[max_index]


def convert(image, dtype):
    """
    Converts `image` to the NumPy `dtype` and scales the intensity values
    accordingly.

    Intensity values are always clipped to the allowed range (even for
    identical source and target types). Returns always a copy of the data,
    even for equal source and target types.
    """

    # clip image against its source dtype (important for floats)
    # clip also guarantees that the original image will remain unchanged
    (lower, upper) = dtype_range(dtype=image.dtype)
    image_clipped = clip(image=image, lower=lower, upper=upper)

    if image.dtype == dtype:
        return image_clipped
    else:
        # only a scale factor is needed, since all dtypes share a common "zero"
        scale = dtype_range(dtype=dtype)[1] / dtype_range(dtype=image.dtype)[1]

        # use at least the 'float32' dtype for the intermediate image (but if the image is 'float64', use that)
        intermediate_dtype = dtype_common(dtypes=[image.dtype, np.float32])

        return (image_clipped.astype(dtype=intermediate_dtype) * scale).astype(dtype)


####
#%%% array access
####


def tir(*args):
    """
    The items of `*args` are rounded, converted to `int` and combined into a
    tuple.

    The primary use-case of this function is to pass point coordinates to
    certain OpenCV functions.

    >>> tir(1.24, -1.87)
    (1, -2)
    """

    if (len(args) == 1) and (len(args[0]) == 2):
        items = args[0]
    elif len(args) == 2:
        items = args
    else:
        raise ValueError("The two required arguments must either be (i) given separately or (ii) via a sequence of length two, but got neither")
    return tuple(int(round(item)) for item in items)


####
#%%% geometry related
####


def size(image):
    """
    Return the size `(X, Y)` of the given image.
    """
    return (image.shape[1], image.shape[0])


def resize(image, scale_or_size, interpolation_down=cv2.INTER_CUBIC, interpolation_up=cv2.INTER_NEAREST):
    if isinstance(scale_or_size, float):
        scale = scale_or_size
        return cv2.resize(src=image, dsize=None, dst=None, fx=scale, fy=scale, interpolation=interpolation_up if scale > 1.0 else interpolation_down)
    
    elif isinstance(scale_or_size, tuple) and (len(scale_or_size) == 2):
        target_size = scale_or_size
        current_size = size(image)
        return cv2.resize(src=image, dsize=target_size, dst=None, fx=0.0, fy=0.0, interpolation=interpolation_up if all(target_size[n_dim] > current_size[n_dim] for n_dim in range(2)) else interpolation_down)
    
    else:
        raise ValueError("Expected a float (= scale factor) or a 2-tuple (= target size) for argument 'scale_or_size', but got type '{}'".format(type(scale_or_size)))


class PaddedImageIndexer():
    """
    Wrapper for an `np.ndarray` which allows indexing out-of-bounds and returns
    a padded image.
    """

    def __init__(self, image, pad_kwargs=None):
        self.image = image
        self.pad_kwargs = pad_kwargs
        if self.pad_kwargs is None:
            self.pad_kwargs = {}

        assert isinstance(self.image, np.ndarray)

    def __getitem__(self, item):
        indices = item
        axis_count = len(self.image.shape)

        if len(indices) != axis_count:
            raise ValueError("The axis count is {}, and does not match the axis count of the image ({})".format(len(indices), axis_count))

        # for each axis collect the in-bound cropping indices and the pad widths
        in_bound_indices = []
        pad_widths = []
        for (n_axis, index) in enumerate(indices):
            if not isinstance(index, slice):
                raise TypeError("All indices must be slices, but index #{} is of type '{}'".format(n_axis, type(index).__name__))
            if (index.step is not None) and (index.step != 1):
                raise ValueError("Step sized != 1 are currently not supported, but index #{} has step size {}".format(n_axis, index.step))

            axis_size = self.image.shape[n_axis]

            # replace None entries of the slice with numbers
            start = index.start if (index.start is not None) else 0
            stop = index.stop if (index.stop is not None) else axis_size

            if start >= stop:
                raise ValueError("Slice start ({}) is not smaller than slice stop ({})".format(start, stop))

            # determine padding at the start of the axis
            if start >= 0:
                pad_before = 0
            else:
                pad_before = -start
                start = 0

            # determine padding at the end of the axis
            if stop <= axis_size:
                pad_after = 0
            else:
                pad_after = stop - axis_size
                stop = axis_size

            # store pad widths and
            in_bound_indices.append(slice(start, stop))
            pad_widths.append((pad_before, pad_after))

        # perform a valid crop within the original image
        image_cropped = self.image[tuple(in_bound_indices)]

        # apply padding where necessary
        image_padded = np.pad(array=image_cropped, pad_width=pad_widths, **self.pad_kwargs)

        return image_padded


def pad(image, count=None, count_top=None, count_right=None, count_bottom=None, count_left=None, mode=cv2.BORDER_CONSTANT, constant_value=0):
    if isinstance(mode, int):
        # assume mode to be one of cv2.BORDER_*
        pass
    elif isinstance(mode, str):
        attr_name = "BORDER_{}".format(mode.upper())
        mode = getattr(cv2, attr_name)
    else:
        raise ValueError("Invalid border mode '{}'".format(mode))

    trbl_all_none = (count_top is None) and (count_right is None) and (count_bottom is None) and (count_left is None)

    if (count is not None) and trbl_all_none:
        # padding counts are given by argument 'count'
        (count_top, count_right, count_bottom, count_left) = dito.utils.get_validated_tuple(x=count, type_=int, count=4, min_value=0, max_value=None)
    elif (count is None) and (not trbl_all_none):
        # padding counts are given by argument 'count_*'
        count_top = 0 if (count_top is None) else count_top
        count_right = 0 if (count_right is None) else count_right
        count_bottom = 0 if (count_bottom is None) else count_bottom
        count_left = 0 if (count_left is None) else count_left
    else:
        raise ValueError("If argument 'count' is set, arguments 'top', 'right', 'bottom', 'left' must be unset (None) and vice versa")

    return cv2.copyMakeBorder(src=image, top=count_top, bottom=count_bottom, left=count_left, right=count_right, borderType=mode, value=constant_value)


def center_pad_to(image, target_size, **kwargs):
    """
    Center pad `image` to the given `target_size` if it is smaller than this target size.
    """
    missing_width = max(0, target_size[0] - image.shape[1])
    missing_height = max(0, target_size[1] - image.shape[0])

    count_top = missing_height // 2
    count_bottom = missing_height - count_top
    count_left = missing_width // 2
    count_right = missing_width - count_left

    return pad(image=image, count=None, count_top=count_top, count_right=count_right, count_bottom=count_bottom, count_left=count_left, **kwargs)


def center_crop_to(image, target_size):
    image_size = size(image=image)
    indices = [None, None, Ellipsis]
    for n_dim in range(2):
        offset = max(0, image_size[n_dim] - target_size[n_dim]) // 2
        indices[1 - n_dim] = slice(offset, min(image_size[n_dim], offset + target_size[n_dim]))
    return image[tuple(indices)]


def center_pad_crop_to(image, target_size, **kwargs):
    image_padded = center_pad_to(image=image, target_size=target_size, **kwargs)
    image_cropped = center_crop_to(image=image_padded, target_size=target_size)
    return image_cropped


def rotate(image, angle_deg, padding_mode=None, interpolation=cv2.INTER_CUBIC):
    """
    Rotate the given `image` by an arbitrary angle given in degrees.
    """
    image_size = size(image=image)

    # determine target image size based on padding mode
    if padding_mode is None:
        # no padding
        target_size = image_size
    elif padding_mode == "tight":
        angle_rad = angle_deg * np.pi / 180.0
        sin_angle = np.abs(np.sin(angle_rad))
        cos_angle = np.abs(np.cos(angle_rad))
        target_size = (
            int(np.ceil(cos_angle * image_size[0] + sin_angle * image_size[1])),
            int(np.ceil(cos_angle * image_size[1] + sin_angle * image_size[0])),
        )
    elif padding_mode == "full":
        diag = int(np.ceil(np.sqrt(image_size[0]**2 + image_size[1]**2)))
        target_size = (diag, diag)
    else:
        raise ValueError("Invalid padding mode '{}'".format(padding_mode))

    # get rotation matrix and change the translation to match the target image size
    rotation_matrix = cv2.getRotationMatrix2D(center=(image.shape[1] // 2, image.shape[0] // 2), angle=angle_deg, scale=1.0)
    rotation_matrix[0, 2] += target_size[0] // 2 - image_size[0] // 2
    rotation_matrix[1, 2] += target_size[1] // 2 - image_size[1] // 2

    return cv2.warpAffine(src=image, M=rotation_matrix, dsize=target_size, flags=interpolation)


def rotate_90(image):
    return cv2.rotate(src=image, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)


def rotate_180(image):
    return cv2.rotate(src=image, rotateCode=cv2.ROTATE_180)


def rotate_270(image):
    return cv2.rotate(src=image, rotateCode=cv2.ROTATE_90_CLOCKWISE)


####
#%%% channel-related
####
    

def is_gray(image):
    """
    Return `True` iff the given image is a grayscale image.
    """
    
    return (len(image.shape) == 2) or ((len(image.shape) == 3) and (image.shape[2] == 1))


def is_color(image):
    """
    Return `True` iff the given image is a color image.
    """
    
    return (len(image.shape) == 3) and (image.shape[2] == 3)


def as_gray(image, keep_color_dimension=False):
    """
    Convert the given image from BGR to grayscale.
    
    If it is already a grayscale image, return the image unchanged.
    """

    if is_gray(image=image):
        image_gray = image
    else:
        image_gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)

    if keep_color_dimension and (len(image_gray.shape) == 2):
        image_gray = image_gray[:, :, np.newaxis]

    return image_gray


def as_color(image):
    """
    Convert the given image from grayscale to BGR.
    
    If it is already a color image, return the image unchanged.
    """
    
    if is_color(image=image):
        return image
    else:
        return cv2.cvtColor(src=image, code=cv2.COLOR_GRAY2BGR)


def convert_color(image_or_color, code):
    if isinstance(image_or_color, tuple) and (1 <= len(image_or_color) <= 3):
        # color mode
        color_array = np.array(image_or_color, dtype=np.uint8)
        color_array.shape = (1, 1, 3)
        return tuple(cv2.cvtColor(src=color_array, code=code)[0, 0, ...].tolist())
    elif dito.core.is_image(image_or_color):
        # image mode
        return cv2.cvtColor(src=image_or_color, code=code)
    else:
        raise ValueError("Argument 'image_or_color' must be an image or a color, but is '{}'".format(type(image_or_color)))


def bgr_to_hsv(image_or_color):
    return convert_color(image_or_color=image_or_color, code=cv2.COLOR_BGR2HSV)


def hsv_to_bgr(image_or_color):
    return convert_color(image_or_color=image_or_color, code=cv2.COLOR_HSV2BGR)


def flip_channels(image):
    """
    Changes BGR channels to RGB channels and vice versa.
    """
    return cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)


def split_channels(image):
    """
    Splits the image into a tuple containing its channels as individual images.
    """
    axis_count = len(image.shape)
    if axis_count == 2:
        return (image,)
    elif axis_count == 3:
        return tuple(image[:, :, n_channel] for n_channel in range(image.shape[2]))
    else:
        raise dito.exceptions.InvalidImageShapeError("Image shape must have two or three axes, but is {}".format(image.shape))


def as_channels(b=None, g=None, r=None):
    """
    Merge up to three gray scale images into one color image.
    """
    # check arguments
    if (b is None) and (g is None) and (r is None):
        raise ValueError("At least for one channel an image must be given")

    # get the first non-`None` image (needed to determine the shape and dtype below)
    for channel_image in (b, g, r):
        if channel_image is not None:
            channel_image_zero = 0 * channel_image
            break

    channel_images = []
    for channel_image in (b, g, r):
        if channel_image is not None:
            if not is_gray(image=channel_image):
                raise ValueError("At least one of the given images is not a gray scale image")
            channel_images.append(channel_image)
        else:
            channel_images.append(channel_image_zero)

    return cv2.merge(mv=channel_images)



####
#%%% value-related
####


def clip(image, lower=None, upper=None):
    """
    Clip values to the range specified by `lower` and `upper`.
    """

    # assert that the input array remains unchanged
    image = image.copy()

    # clip
    if lower is not None:
        image[image < lower] = lower
    if upper is not None:
        image[image > upper] = upper

    return image


def clip_01(image):
    """
    Clip values to the range `(0.0, 1.0)`.
    """
    return clip(image=image, lower=0.0, upper=1.0)


def clip_11(image):
    """
    Clip values to the range `(-1.0, 1.0)`.
    """
    return clip(image=image, lower=-1.0, upper=1.0)


def normalize(image, mode="minmax", **kwargs):
    """
    Normalizes the intensity values of the given image.
    """

    if mode == "none":
        return image

    elif mode == "interval":
        # interval range to be spread out to the "full" interval range
        (lower_source, upper_source) = sorted((kwargs["lower"], kwargs["upper"]))

        # the target interval range depends on the image's data type
        (lower_target, upper_target) = dtype_range(image.dtype)

        # we temporarily work with a float image (because values outside of
        # the target interval can occur)
        image_work = image.astype("float").copy()
        
        # spread the given interval to the full range, clip outlier values
        image_work = (image_work - lower_source) / (upper_source - lower_source) * (upper_target - lower_target) + lower_target
        image_work = clip(image=image_work, lower=lower_target, upper=upper_target)

        # return an image with the original data type
        return image_work.astype(image.dtype)

    elif mode == "minmax":
        return normalize(image, mode="interval", lower=np.min(image), upper=np.max(image))

    elif mode == "zminmax":
        # "zero-symmetric" minmax (makes only sense for float images)
        absmax = max(np.abs(np.min(image)), np.abs(np.max(image)))
        return normalize(image, mode="interval", lower=-absmax, upper=absmax)

    elif mode == "percentile":
        for key in ("q", "p"):
            if key in kwargs.keys():
                q = kwargs[key]
                break
        else:
            q = 2.0
        q = min(max(0.0, q), 50.0)
        return normalize(image, mode="interval", lower=np.percentile(image, q), upper=np.percentile(image, 100.0 - q))

    else:
        raise ValueError("Invalid mode '{mode}'".format(mode=mode))


def invert(image):
    if is_integer_image(image=image) or is_float_image(image=image):
        image_dtype_range = dtype_range(dtype=image.dtype)
        if float(image_dtype_range[0]) != 0.0:
            raise ValueError("Argument 'image' must have dtype with min value of zero (but has dtype '{}')".format(image.dtype))
        return image_dtype_range[1] - image

    elif is_bool_image(image=image):
        return np.logical_not(image)

    else:
        raise ValueError("Unsupported image dtype '{}'".format(image.dtype))
