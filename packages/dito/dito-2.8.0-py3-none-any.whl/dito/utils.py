import collections
import datetime
import errno
import os
import tempfile

import cv2
import numpy as np


####
#%%% OpenCV-related
####


def cv2_version():
    return tuple(int(value) for value in cv2.__version__.split("."))


####
#%%% checks
####


def get_validated_tuple(x, type_, count, min_value=None, max_value=None):
    error_text = "Argument must be a scalar or a {}-tuple/list of type '{}' (min_value={}, max_value={})".format(count, type_, min_value, max_value)

    # check tuple/list
    if isinstance(x, tuple):
        pass
    elif isinstance(x, list):
        x = tuple(x)
    elif isinstance(x, type_):
        x = (x,) * count
    else:
        raise ValueError(error_text)

    # check length
    if len(x) != count:
        raise ValueError(error_text)

    # check value ranges
    for value in x:
        if ((min_value is not None) and (value < min_value)) or ((max_value is not None) and (value > max_value)):
            raise ValueError(error_text)

    return x


####
#%%% number-related
####


def adaptive_round(number, digit_count=4):
    """
    Rounds a number to the first `digit_count` digits after the appearance of
    the first non-zero digit.

    This function supports Python `float`s and `int`s as well as NumPy scalars
    of any type (e.g., `np.float32`, `np.uint8`, etc.).
    """

    with np.errstate(divide="ignore"):
        try:
            magnitude = np.floor(np.log10(np.abs(number)))
        except ValueError:
            magnitude = 0
    if not np.isfinite(magnitude):
        magnitude = 0

    round_digit_count = int(digit_count - magnitude - 1)
    return round(number, round_digit_count)


####
#%%% file-related
####


def mkdir(dirname):
    """
    Create the given directory if it does not already exist.
    """
    
    if dirname == "":
        return
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def get_temp_dir(prefix):
    """
    Creates and returns temporary directory.

    The property `.name` holds the path. It can be deleted using the `.cleanup()` method.
    """
    return tempfile.TemporaryDirectory(prefix=prefix)


def human_bytes(byte_count):
    """
    Formats a given `byte_count` into a human-readable string.
    """

    prefixes = collections.OrderedDict()
    prefixes["KiB"] = 1024.0**1
    prefixes["MiB"] = 1024.0**2
    prefixes["GiB"] = 1024.0**3

    count = byte_count
    unit = "bytes"
    for (new_unit, new_scale) in prefixes.items():
        new_count = byte_count / new_scale
        if new_count < 1.0:
            break
        else:
            count = new_count
            unit = new_unit

    if isinstance(count, int):
        # count is an integer -> use no decimal places
        return "{} {}".format(count, unit)
    else:
        # count is a float -> use two decimal places
        return "{:.2f} {}".format(count, unit)


####
#%%% output-related
####


def now_str(mode="compact", date=True, time=True, microtime=True):
    """
    Return the current date and/or time as string.
    """

    # check arguments
    if not (date or time or microtime):
        raise ValueError("At least one of 'date', 'time', 'microtime' must be `True`")

    # select format string parts based on mode
    if mode == "compact":
        date_fmt = "%Y%m%d"
        time_sep = "_"
        time_fmt = "%H%M%S"
        micro_sep = "_"
        micro_fmt = "%f"
    elif mode == "readable":
        date_fmt = "%Y-%m-%d"
        time_sep = "__"
        time_fmt = "%H-%M-%S"
        micro_sep = "__"
        micro_fmt = "%f"
    elif mode == "print":
        date_fmt = "%Y-%m-%d"
        time_sep = " "
        time_fmt = "%H:%M:%S"
        micro_sep = "."
        micro_fmt = "%f"
    else:
        raise ValueError("Invalid mode '{}".format(mode))

    # build final format string
    fmt = ""
    if date:
        fmt += date_fmt
    if time:
        if fmt != "":
            fmt += time_sep
        fmt += time_fmt
    if microtime:
        if fmt != "":
            fmt += micro_sep
        fmt += micro_fmt

    # return formatted date and/or time
    return datetime.datetime.now().strftime(fmt)


def ftable(rows, first_row_is_header=False):
    """
    Format the data specified in `rows` as table string.
    """
    
    col_sep = "  "
    sep_symbol = "-"
    
    # count the max length for each column
    col_count = max(len(row) for row in rows)
    col_lengths = [0] * col_count
    for row in rows:
        for n_col in range(col_count):
            col_lengths[n_col] = max(col_lengths[n_col], len(str(row[n_col])))

    # the line at the top and bottom
    sep_line = col_sep.join(sep_symbol * col_length for col_length in col_lengths)
    
    # transform rows into lines
    lines = []
    lines.append(sep_line)
    for (n_row, row) in enumerate(rows):
        col_strs = []
        for (col_length, col) in zip(col_lengths, row):
            col_str = "{{: <{}}}".format(col_length).format(str(col))
            col_strs.append(col_str)
        lines.append(col_sep.join(col_strs))
        if first_row_is_header and (n_row == 0):
            lines.append(sep_line)
    lines.append(sep_line)
    
    # return table as single string
    return "\n".join(lines)
    

def ptable(rows, ftable_kwargs=None, print_kwargs=None):
    """
    Print the data specified in `rows` as table.
    """

    if ftable_kwargs is None:
        ftable_kwargs = {}
    if print_kwargs is None:
        print_kwargs = {}

    print(ftable(rows=rows, **ftable_kwargs), **print_kwargs)
