import json
import os
import numpy as np
from scipy import stats
from yolo_categories import CATEGORIES_REVERSED


def count_classes(dir='data/dataset', simple_count=False):
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

    counter = {}

    if (simple_count):
        # We suppose that the name is as AJGH23.txt
        for filename in txt_filenames:
            for letter in filename.split('.')[0]:
                counter[letter] = 1 if not letter in counter else counter[letter] + 1
        return counter

    else:
        for filename in txt_filenames:
            with open("{0}/{1}".format(dir, filename), 'r') as f:
                for line in f.read().split("\n"):
                    class_number = line.split(" ")[0]
                    if class_number != "":
                        if class_number in counter:
                            counter[class_number] += 1
                        else:
                            counter[class_number] = 1
        # Reverse and show the class name and not the number
        final_result = {}
        for key in counter:
            final_result[CATEGORIES_REVERSED[int(key)]] = counter[key]
        return final_result


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


data = count_classes()
print_some_stats(data)
print("Sorted:", sort_by_quantity(data))
print("Data: \n", json.dumps(data, indent=2, sort_keys=True))
