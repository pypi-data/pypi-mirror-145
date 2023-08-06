import abc
import collections

import cv2
import numpy as np

import dito

try:
    import sklearn.decomposition
    SKLEARN_IMPORT_ERROR = None
except ImportError as e:
    SKLEARN_IMPORT_ERROR = e


class DecompositionTextureModel(abc.ABC):
    def __init__(self, images, component_count, keep_images=True):
        if SKLEARN_IMPORT_ERROR is not None:
            raise SKLEARN_IMPORT_ERROR

        # save images
        self.image_count = len(images)
        if self.image_count == 0:
            raise ValueError("No images were given")
        self.image_shape = images[0].shape
        self.image_dtype = images[0].dtype

        self.component_count = component_count
        self.keep_images = keep_images

        # estimate decomposition
        self.X = np.array(images).reshape(self.image_count, -1)
        self.fit_decomposition()

        # project input images into the parameter space
        if self.keep_images:
            self.P = self.decomposition.transform(self.X)
        else:
            self.X = np.zeros(shape=(0, self.X.shape[1]), dtype=self.X.dtype)
            self.P = np.zeros_like(self.X, dtype=np.float32)

        # needed for the interactive visualization
        self.image_window_name = "TextureModel - Images"
        self.slider_window_name = "TextureModel - Sliders"

    @abc.abstractmethod
    def fit_decomposition(self, *args, **kwargs):
        pass

    ##
    ## conversion between images, image vectors (x) and parameter vectors (p)
    ##

    @staticmethod
    def image_to_x(image):
        return image.reshape(1, -1)[0, :]

    def x_to_image(self, x):
        image = x.reshape(*self.image_shape)
        dtype_range = dito.core.dtype_range(dtype=self.image_dtype)
        image = dito.core.clip(image, *dtype_range)
        image = image.astype(self.image_dtype)
        return image

    def x_to_p(self, x):
        return self.decomposition.transform(x.reshape(1, -1))[0, :]

    def p_to_x(self, p):
        return self.decomposition.inverse_transform(p.reshape(1, -1))[0, :]

    def image_to_p(self, image):
        x = self.image_to_x(image)
        p = self.x_to_p(x)
        return p

    def p_to_image(self, p):
        x = self.p_to_x(p)
        image = self.x_to_image(x)
        return image

    def get_random_p(self):
        return np.random.normal(loc=0.0, scale=1.0, size=(self.component_count,))

    ##
    ## visualization
    ##

    def create_sliders(self, slider_range):
        sliders = collections.OrderedDict()
        sliders["sample"] = dito.highgui.IntegerSlider(
            window_name=self.slider_window_name,
            name="sample",
            min_value=0,
            max_value=self.image_count - 1,
        )
        for n_component in range(self.component_count):
            slider_name = "C{}".format(n_component + 1)
            sliders[slider_name] = dito.highgui.FloatSlider(
                window_name=self.slider_window_name,
                name=slider_name,
                min_value=slider_range[0],
                initial_value=0.0,
                max_value=slider_range[1],
                value_count=255,
            )
        return sliders

    def get_p_from_sliders(self, sliders):
        p = np.zeros(shape=(self.component_count,), dtype=np.float32)
        for n_component in range(self.component_count):
            slider_name = "C{}".format(n_component + 1)
            p[n_component] = sliders[slider_name].get_value()
        return p

    def get_image_from_sliders(self, sliders):
        p = self.get_p_from_sliders(sliders)
        image = self.p_to_image(p)
        return image

    def set_sliders_from_p(self, sliders, p):
        for n_component in range(self.component_count):
            slider_name = "C{}".format(n_component + 1)
            sliders[slider_name].set_value(float(p[n_component]))

    def reset_sliders(self, sliders):
        p = np.zeros(shape=(self.component_count,), dtype=np.float32)
        self.set_sliders_from_p(sliders=sliders, p=p)

    def invert_sliders(self, sliders):
        p = self.get_p_from_sliders(sliders)
        self.set_sliders_from_p(sliders=sliders, p=-p)

    def randomize_sliders(self, sliders):
        p = self.get_random_p()
        self.set_sliders_from_p(sliders=sliders, p=p)

    def perturb_sliders(self, sliders):
        p = self.get_p_from_sliders(sliders)
        dp = self.get_random_p() * 0.1
        self.set_sliders_from_p(sliders=sliders, p=p + dp)

    def run_interactive(self, slider_range=(-3.0, 3.0)):
        cv2.namedWindow(self.image_window_name)
        cv2.namedWindow(self.slider_window_name)
        sliders = self.create_sliders(slider_range=slider_range)

        while True:
            if sliders["sample"].changed:
                n_sample = sliders["sample"].get_value()
                if n_sample < self.X.shape[0]:
                    x = self.X[n_sample, :]
                    p = self.x_to_p(x)
                else:
                    p = np.zeros(shape=(self.component_count,), dtype=np.float32)
                self.set_sliders_from_p(sliders, p)

            if any(slider.changed for (slider_name, slider) in sliders.items() if slider.name != "sample"):
                image = self.get_image_from_sliders(sliders)

            key = dito.visual.show(image, wait=10, window_name=self.image_window_name)
            if key in dito.visual.qkeys():
                # quit
                break
            elif key == ord("+"):
                # go to the next image
                sliders["sample"].set_value((sliders["sample"].get_value() + 1) % self.image_count)
            elif key == ord("-"):
                # go to the previous image
                sliders["sample"].set_value((sliders["sample"].get_value() - 1) % self.image_count)
            elif key == ord("n"):
                # set all parameter sliders to zero
                self.reset_sliders(sliders)
            elif key == ord("i"):
                # invert all parameter sliders
                self.invert_sliders(sliders)
            elif key == ord("r"):
                # randomize all parameter sliders
                self.randomize_sliders(sliders)
            elif key == ord("p"):
                # randomly perturb all parameter sliders
                self.perturb_sliders(sliders)
            elif key == ord("s"):
                # save current image
                image_filename = dito.io.save_tmp(image)
                print("Saved image as '{}'".format(image_filename))


class PcaTextureModel(DecompositionTextureModel):
    def fit_decomposition(self):
        self.decomposition = sklearn.decomposition.PCA(
            n_components=self.component_count,
            whiten=True,
        )
        self.decomposition.fit(self.X)


class NmfTextureModel(DecompositionTextureModel):
    def fit_decomposition(self):
        self.decomposition = sklearn.decomposition.NMF(
            n_components=self.component_count,
        )
        self.decomposition.fit(self.X)
