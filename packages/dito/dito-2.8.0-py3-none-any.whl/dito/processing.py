import math
import operator

import cv2
import numpy as np

import dito.core
import dito.visual


##
## basic processing
##


def gaussian_blur(image, sigma):
    if sigma <= 0.0:
        return image
    return cv2.GaussianBlur(src=image, ksize=None, sigmaX=sigma)


def median_blur(image, kernel_size):
    return cv2.medianBlur(src=image, ksize=kernel_size)


def clahe(image, clip_limit=None, tile_grid_size=None):
    clahe_op = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe_op.apply(image)


##
## thresholding
##


def otsu(image):
    if dito.core.is_color(image=image):
        raise ValueError("Expected gray image but got color image for Otsu thresholding")
    (theta, image2) = cv2.threshold(src=image, thresh=-1, maxval=255, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return (theta, image2)


def otsu_theta(image):
    (theta, image2) = otsu(image=image)
    return theta


def otsu_image(image):
    (theta, image2) = otsu(image=image)
    return image2


##
## morphological operations
##


def morpho_op_kernel(shape, size):
    ksize = dito.utils.get_validated_tuple(x=size, type_=int, count=2)
    kernel = cv2.getStructuringElement(shape=shape, ksize=ksize, anchor=(-1, -1))
    return kernel


def morpho_op(image, operation, shape=cv2.MORPH_ELLIPSE, size=3, anchor=(-1, -1), iterations=1):
    kernel = morpho_op_kernel(shape=shape, size=size)
    return cv2.morphologyEx(src=image, op=operation, kernel=kernel, anchor=anchor, iterations=iterations)


def dilate(image, **kwargs):
    return morpho_op(image=image, operation=cv2.MORPH_DILATE, **kwargs)


def erode(image, **kwargs):
    return morpho_op(image=image, operation=cv2.MORPH_ERODE, **kwargs)


def morpho_open(image, **kwargs):
    return morpho_op(image=image, operation=cv2.MORPH_OPEN, **kwargs)


def morpho_close(image, **kwargs):
    return morpho_op(image=image, operation=cv2.MORPH_CLOSE, **kwargs)


def blackhat(image, **kwargs):
    return morpho_op(image=image, operation=cv2.MORPH_BLACKHAT, **kwargs)


def tophat(image, **kwargs):
    return morpho_op(image=image, operation=cv2.MORPH_TOPHAT, **kwargs)


##
## filters
##


def dog(image, sigma1, sigma2, return_raw=False, colormap=None):
    blur1 = gaussian_blur(image=image, sigma=sigma1).astype(np.float32)
    blur2 = gaussian_blur(image=image, sigma=sigma2).astype(np.float32)
    diff = blur1 - blur2
    if return_raw:
        return diff
    else:
        diff_11 = diff / dito.core.dtype_range(dtype=image.dtype)[1]
        diff_01 = (diff_11 + 1.0) * 0.5
        result = dito.convert(image=diff_01, dtype=image.dtype)
        if colormap is not None:
            result = dito.visual.colorize(image=result, colormap=colormap)
        return result


def dog_interactive(image, colormap=None):
    window_name = "dito.dog_interactive"
    sliders = [dito.highgui.FloatSlider(window_name=window_name, name="sigma{}".format(n_slider + 1), min_value=0.0, max_value=15.0, value_count=1001) for n_slider in range(2)]
    sliders[0].set_value(0.5)
    sliders[1].set_value(0.8)

    image_show = None
    while True:
        if (image_show is None) or any(slider.changed for slider in sliders):
            sigmas = [sliders[n_slider].get_value() for n_slider in range(2)]
            images_blur = [gaussian_blur(image=image, sigma=sigmas[n_slider]) for n_slider in range(2)]
            images_blur = [dito.visual.text(image=image_blur, message="sigma{} = {:.2f}".format(n_slider + 1, sigmas[n_slider])) for (n_slider, image_blur) in enumerate(images_blur)]
            image_dog = dog(image, sigma1=sigmas[0], sigma2=sigmas[1], return_raw=False, colormap=colormap)
            image_show = dito.stack([[image, image_dog], images_blur])
        key = dito.show(image=image_show, window_name=window_name, wait=10)
        if key in dito.qkeys():
            return


##
## contours
##


class Contour():
    def __init__(self, points):
        self.points = points

    def __len__(self):
        """
        Returns the number of points.
        """
        return len(self.points)

    def __eq__(self, other):
        if not isinstance(other, Contour):
            raise TypeError("Argument 'other' must be a contour")

        if len(self) != len(other):
            return False

        return np.array_equal(self.points, other.points)

    def copy(self):
        return Contour(points=self.points.copy())

    def get_center(self):
        return np.mean(self.points, axis=0)

    def get_center_x(self):
        return np.mean(self.points[:, 0])

    def get_center_y(self):
        return np.mean(self.points[:, 1])

    def get_min_x(self):
        return np.min(self.points[:, 0])

    def get_max_x(self):
        return np.max(self.points[:, 0])

    def get_width(self):
        return self.get_max_x() - self.get_min_x()

    def get_min_y(self):
        return np.min(self.points[:, 1])

    def get_max_y(self):
        return np.max(self.points[:, 1])

    def get_height(self):
        return self.get_max_y() - self.get_min_y()

    def get_area(self, mode="draw"):
        if mode == "draw":
            image = self.draw_standalone(color=(1,), thickness=1, filled=True, antialias=False, border=2)
            return np.sum(image)

        elif mode == "calc":
            return cv2.contourArea(contour=self.points)

        else:
            raise ValueError("Invalid value for argument 'mode': '{}'".format(mode))

    def get_perimeter(self):
        return cv2.arcLength(curve=self.points, closed=True)

    def get_circularity(self):
        r_area = np.sqrt(self.get_area() / np.pi)
        r_perimeter = self.get_perimeter() / (2.0 * np.pi)
        return r_area / r_perimeter

    def get_ellipse(self):
        return cv2.fitEllipse(points=self.points)

    def get_eccentricity(self):
        ellipse = self.get_ellipse()
        (width, height) = ellipse[1]
        semi_major_axis = max(width, height) * 0.5
        semi_minor_axis = min(width, height) * 0.5
        eccentricity = math.sqrt(1.0 - (semi_minor_axis / semi_major_axis)**2)
        return eccentricity

    def get_moments(self):
        return cv2.moments(array=self.points, binaryImage=False)

    def get_hu_moments(self, log=True):
        hu_moments = cv2.HuMoments(m=self.get_moments())
        if log:
            return np.sign(hu_moments) * np.log10(np.abs(hu_moments))
        else:
            return hu_moments

    def shift(self, offset_x=None, offset_y=None):
        if offset_x is not None:
            self.points[:, 0] += offset_x
        if offset_y is not None:
            self.points[:, 1] += offset_y

    def draw(self, image, color, thickness=1, filled=True, antialias=False, offset=None):
        cv2.drawContours(image=image, contours=[np.round(self.points).astype(np.int)], contourIdx=0, color=color, thickness=cv2.FILLED if filled else thickness, lineType=cv2.LINE_AA if antialias else cv2.LINE_8, offset=offset)

    def draw_standalone(self, color, thickness=1, filled=True, antialias=False, border=0):
        image = np.zeros(shape=(2 * border + self.get_height(), 2 * border + self.get_width()), dtype=np.uint8)
        self.draw(image=image, color=color, thickness=thickness, filled=filled, antialias=antialias, offset=(border - self.get_min_x(), border - self.get_min_y()))
        return image


class ContourList():
    def __init__(self, contours):
        self.contours = contours

    def __len__(self):
        """
        Returns the number of found contours.
        """
        return len(self.contours)

    def __eq__(self, other):
        if not isinstance(other, ContourList):
            raise TypeError("Argument 'other' must be a contour list")

        if len(self) != len(other):
            return False

        for (contour_self, contour_other) in zip(self.contours, other.contours):
            if contour_self != contour_other:
                return False

        return True

    def __getitem__(self, key):
        return self.contours[key]

    def copy(self):
        contours_copy = [contour.copy() for contour in self.contours]
        return ContourList(contours=contours_copy)

    def filter(self, func, min_value=None, max_value=None):
        if (min_value is None) and (max_value is None):
            # nothing to do
            return

        # filter
        contours_filtered = []
        for contour in self.contours:
            value = func(contour)
            if (min_value is not None) and (value < min_value):
                continue
            if (max_value is not None) and (value > max_value):
                continue
            contours_filtered.append(contour)
        self.contours = contours_filtered

    def filter_center_x(self, min_value=None, max_value=None):
        self.filter(func=operator.methodcaller("get_center_x"), min_value=min_value, max_value=max_value)

    def filter_center_y(self, min_value=None, max_value=None):
        self.filter(func=operator.methodcaller("get_center_y"), min_value=min_value, max_value=max_value)

    def filter_area(self, min_value=None, max_value=None, mode="draw"):
        self.filter(func=operator.methodcaller("get_area", mode=mode), min_value=min_value, max_value=max_value)

    def filter_perimeter(self, min_value=None, max_value=None):
        self.filter(func=operator.methodcaller("get_perimeter"), min_value=min_value, max_value=max_value)

    def filter_circularity(self, min_value=None, max_value=None):
        self.filter(func=operator.methodcaller("get_circularity"), min_value=min_value, max_value=max_value)

    def find_largest(self, return_index=True):
        """
        Returns the index of the largest (area-wise) contour.
        """
        max_area = None
        argmax_area = None
        for (n_contour, contour) in enumerate(self.contours):
            area = contour.get_area()
            if (max_area is None) or (area > max_area):
                max_area = area
                argmax_area = n_contour

        if argmax_area is None:
            return None
        else:
            if return_index:
                return argmax_area
            else:
                return self.contours[argmax_area]

    def draw_all(self, image, colors=None, **kwargs):
        if colors is None:
            colors = tuple(dito.random_color() for _ in range(len(self)))

        for (contour, color) in zip(self.contours, colors):
            contour.draw(image=image, color=color, **kwargs)


class ContourFinder(ContourList):
    def __init__(self, image):
        self.image = image.copy()
        if self.image.dtype == np.bool:
            self.image = dito.core.convert(image=self.image, dtype=np.uint8)
        contours = self.find_contours(image=self.image)
        super().__init__(contours=contours)

    @staticmethod
    def find_contours(image):
        """
        Called internally to find the contours in the given `image`.
        """

        # find raw contours
        result = cv2.findContours(image=image, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE)

        # compatible with OpenCV 3.x and 4.x, see https://stackoverflow.com/a/53909713/1913780
        contours_raw = result[-2]

        # return tuple of instances of class `Contour`
        return [Contour(points=contour_raw[:, 0, :]) for contour_raw in contours_raw]


def contours(image):
    """
    Convenience wrapper for `ContourFinder`.
    """
    contour_finder = ContourFinder(image=image)
    return contour_finder.contours


class VoronoiPartition(ContourList):
    def __init__(self, image_size, points):
        contours = self.get_facets(image_size=image_size, points=points)
        super().__init__(contours=contours)

    @staticmethod
    def get_facets(image_size, points):
        subdiv = cv2.Subdiv2D((0, 0, image_size[0], image_size[1]))
        for point in points:
            subdiv.insert(pt=point)
        (voronoi_facets, voronoi_centers) = subdiv.getVoronoiFacetList(idx=[])
        return [Contour(voronoi_facet) for voronoi_facet in voronoi_facets]


def voronoi(image_size, points):
    voronoi_partition = VoronoiPartition(image_size=image_size, points=points)
    return voronoi_partition.contours
