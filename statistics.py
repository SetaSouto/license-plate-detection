import os
import numpy as np
from scipy import stats


def count_classes(dir='data/generated_plates', simple_count=True):
    """
    Given a directory returns a dict with all the classes found and the quantity if each class. It counts over the
    .txt files.
    Result:
    {
        "A": 150, "B": ...
    }

    :param simple_count: Boolean indicating if it only has to count by the name of the file (less expensive).
    """
    # Get only txt files
    txt_filenames = list(filter(lambda x: x[-3:] == 'txt', os.listdir(dir)))
    if (simple_count):
        # We suppose that the name is as AJGH23.txt
        counter = {}
        for filename in txt_filenames:
            for letter in filename.split('.')[0]:
                counter[letter] = 1 if not letter in counter else counter[letter] + 1
        return counter
    else:
        raise NotImplementedError()


def max_from_json(data):
    """
    Returns the max value (and its class) in a dict of pairs key: value (Integer).
    """
    result = (None, -1)
    for key in data:
        if data[key] > max: result = (key, data[key])
    return result


def sort_by_quantity(data):
    """
    Returns a list ordered by the quantity of the class. Works with the output of count_classes.
    """
    return sorted(data.items(), key=lambda x: x[1])


def print_some_stats(data):
    """
    Prints the mean, mode and variances of the data.
    """
    print(stats.describe(np.array(list(data.values()))))


print_some_stats(count_classes())
