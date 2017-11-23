"""
Script to clean the txt generated files and kept only the 37 class: LICENSE-PLATE and set the number 0 to the class.
"""
import os

dataset_dir = "data/dataset/"

for filename in list(filter(lambda x: x[-3:] == "txt", os.listdir(dataset_dir))):
    with open(dataset_dir + filename, 'r') as f:
        content = f.read()
    with open(dataset_dir + filename, 'w') as f:
        license_plate_lines = filter(lambda x: x.split(' ')[0] == "37", content.split('\n'))
        for line in license_plate_lines:
            line = line.split(' ')
            line[0] = "0"
            line = ' '.join(line)
            f.write(line)
