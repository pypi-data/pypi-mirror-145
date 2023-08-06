import abc
import copy

import cv2

import dito.visual


class Slider(abc.ABC):
    def __init__(self, window_name, name, initial_raw_value, max_raw_value):
        assert max_raw_value > 0
        assert 0 <= initial_raw_value <= max_raw_value

        self.window_name = window_name
        if self.window_name is None:
            self.window_name = dito.visual.DEFAULT_WINDOW_NAME
        self.name = name
        self.initial_raw_value = initial_raw_value
        self.max_raw_value = max_raw_value

        self.create_trackbar()
        self.changed = True

    def callback(self, raw_value):
        self.changed = True
        self.custom_callback()

    def custom_callback(self):
        pass

    def create_trackbar(self):
        cv2.namedWindow(winname=self.window_name)
        cv2.createTrackbar(self.name, self.window_name, self.initial_raw_value, self.max_raw_value, self.callback)

    def get_raw_value(self):
        self.changed = False
        return cv2.getTrackbarPos(trackbarname=self.name, winname=self.window_name)

    def set_raw_value(self, raw_value):
        if raw_value < 0:
            raw_value = 0
        elif raw_value > self.max_raw_value:
            raw_value = self.max_raw_value
        cv2.setTrackbarPos(trackbarname=self.name, winname=self.window_name, pos=raw_value)

    def reset(self):
        self.set_raw_value(raw_value=self.initial_raw_value)

    @abc.abstractmethod
    def raw_from_value(self, value):
        pass

    @abc.abstractmethod
    def value_from_raw(self, raw_value):
        pass

    def get_value(self):
        raw_value = self.get_raw_value()
        return self.value_from_raw(raw_value=raw_value)

    def set_value(self, value):
        raw_value = self.raw_from_value(value=value)
        self.set_raw_value(raw_value=raw_value)


class ChoiceSlider(Slider):
    def __init__(self, window_name, name, choices, initial_choice=None):
        self.choices = copy.deepcopy(choices)
        super().__init__(
            name=name,
            window_name=window_name,
            initial_raw_value=0 if initial_choice is None else self.raw_from_value(value=initial_choice),
            max_raw_value=len(self.choices) - 1,
        )

    def raw_from_value(self, value):
        return self.choices.index(value)

    def value_from_raw(self, raw_value):
        return self.choices[raw_value]


class BoolSlider(Slider):
    def __init__(self, window_name, name, initial_value=False):
        super().__init__(
            name=name,
            window_name=window_name,
            initial_raw_value=self.raw_from_value(value=initial_value),
            max_raw_value=1,
        )

    def raw_from_value(self, value):
        return 1 if value else 0

    def value_from_raw(self, raw_value):
        return raw_value > 0


class IntegerSlider(Slider):
    def __init__(self, window_name, name, min_value, max_value, initial_value=None):
        self.min_value = min_value
        self.max_value = max_value

        super().__init__(
            name=name,
            window_name=window_name,
            initial_raw_value=self.raw_from_value(value=self.resolve_initial_value(initial_value=initial_value)),
            max_raw_value=self.max_value - self.min_value,
        )

    def resolve_initial_value(self, initial_value):
        if isinstance(initial_value, int):
            return initial_value
        if initial_value is None:
            return self.min_value
        if initial_value == "min":
            return self.min_value
        if initial_value == "max":
            return self.max_value
        if initial_value == "mean":
            return (self.max_value - self.min_value) // 2 + self.min_value
        raise RuntimeError("Invalid initial value '{}'".format(initial_value))

    def raw_from_value(self, value):
        return value - self.min_value

    def value_from_raw(self, raw_value):
        return self.min_value + raw_value


class FloatSlider(Slider):
    def __init__(self, window_name, name, min_value, max_value, value_count=101, initial_value=None):
        self.min_value = min_value
        self.max_value = max_value
        self.value_count = value_count

        super().__init__(
            name=name,
            window_name=window_name,
            initial_raw_value=self.raw_from_value(value=self.resolve_initial_value(initial_value=initial_value)),
            max_raw_value=self.value_count - 1,
        )

    def resolve_initial_value(self, initial_value):
        if isinstance(initial_value, float):
            return initial_value
        if initial_value is None:
            return self.min_value
        if initial_value == "min":
            return self.min_value
        if initial_value == "max":
            return self.max_value
        if initial_value == "mean":
            return (self.max_value - self.min_value) * 0.5 + self.min_value
        raise RuntimeError("Invalid initial value '{}'".format(initial_value))

    def raw_from_value(self, value):
        # int is required for the case that `value` is a NumPy float
        return int(round((value - self.min_value) / (self.max_value - self.min_value) * (self.value_count - 1)))

    def value_from_raw(self, raw_value):
        return raw_value / (self.value_count - 1) * (self.max_value - self.min_value) + self.min_value
