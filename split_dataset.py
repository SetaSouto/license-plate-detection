import os

import numpy as np

data_dir = "data/dataset/"
jpg_filenames = list(filter(lambda x: x[-3:] == "jpg", os.listdir(data_dir)))

# Randomly select the test dataset
test_percentage = 0.1
n_test = int(round(len(jpg_filenames) * test_percentage))
if n_test == 0: n_test = 1

# Randomly select the images for testing
test_indexes = np.random.choice(len(jpg_filenames), n_test, replace=False)
test_indexes = set(test_indexes.astype(int))

train_indexes = set(np.arange(len(jpg_filenames))) - test_indexes

with open("test.txt", "w") as f:
    for index in test_indexes:
        f.write(data_dir + jpg_filenames[index] + "\n")

with open("train.txt", "w") as f:
    for index in train_indexes:
        f.write(data_dir + jpg_filenames[index] + "\n")
