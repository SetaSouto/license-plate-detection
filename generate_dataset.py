"""
Script to clean the txt generated files and kept only the 37 class: LICENSE-PLATE and set the number 0 to the class.
"""
import argparse
import os

from image_plate_generator import ImageGenerator
from plate_generator import PlateGenerator
from split_dataset import split_dataset
from CLASSES import CLASSES, CLASSES_REVERSED

# Parse arguments
parser = argparse.ArgumentParser(description='Generate the dataset to train YOLO to detect and read license plates.')
parser.add_argument('--n_plates', type=int, default=500,
                    help='Indicates the number of different plates to generate.')
parser.add_argument('--plates_per_image', type=int, default=2,
                    help='Indicate the number of plates per image in the dataset.')
parser.add_argument('--n_samples_per_image', type=int, default=1,
                    help='Optional. Indicates how many times an image must be used to create a sample for the dataset.')
parser.add_argument('--classes', type=str, nargs='*', default=["LICENSE-PLATE"],
                    help='Indicates the the classes to set in the label file per image.')
parser.add_argument('--dataset_dir', type=str, default='data/dataset',
                    help='Indicates the directory where write the files.')
parser.add_argument('--plates_dir', type=str, default='data/generated_plates',
                    help='Directory where to put the generated plates.')
parser.add_argument('--no_clean', const=True, default=False, nargs='?',
                    help='If presents, does not delete all the files in the dataset dir.')
parser.add_argument('--only_clean_txt', const=True, default=False, nargs='?',
                    help='If present, does not generate any data, only clean the txt files (labels and bounding boxes) with the given classes (with --classes).')
args = parser.parse_args()

print("Working with the following arguments:")
print("   Number of plates:\t\t{0}".format(args.n_plates))
print("   Plates per image:\t\t{0}".format(args.plates_per_image))
print("   Number of samples per image:\t{0}".format(args.n_samples_per_image))
print("   Classes:\t\t\t{0}".format(sorted(list(set((args.classes))))))
print("   Plates directory:\t\t{0}".format(args.plates_dir))
print("   Dataset directory:\t\t{0}".format(args.dataset_dir))
print("   Clean directory:\t\t{0}".format(not args.no_clean))
print("   Only clean txt:\t\t{0}".format(args.only_clean_txt))
print(" ")

if not args.only_clean_txt:
    # Clean directory
    if not args.no_clean:
        for dir in (args.dataset_dir, args.plates_dir):
            print("Cleaning directory {0}".format(dir))
            for filename in os.listdir(dir):
                file_path = os.path.join(dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    # Generate the plates
    PlateGenerator().generate_random_plates(args.n_plates,
                                            show_bounding_box=False,
                                            show=False,
                                            save=True,
                                            debug_bounding_box_normalized=False)

    # Generate the images
    for _ in range(args.n_samples_per_image):
        ImageGenerator().make_images(plates_by_image=args.plates_per_image,
                                     repeat=False,
                                     min_image_percentage=0.1,
                                     max_image_percentage=0.4,
                                     allow_crop=False,
                                     paste_over=False)

    # Split the dataset between test and train
    split_dataset()

# Filter the classes on the labels
classes = sorted(list(set(map(lambda x: str(CLASSES[x]), args.classes))))
print("Classes order: {0}".format(classes))
for filename in list(filter(lambda x: x[-3:] == "txt", os.listdir(args.dataset_dir))):
    # Read the txt file
    file_path = os.path.join(args.dataset_dir, filename)
    with open(file_path, 'r') as f:
        content = f.read()
    # Write the new content
    with open(file_path, 'w') as f:
        license_plate_lines = filter(lambda x: x.split(' ')[0] in classes,  # Keep only the indicated classes
                                     content.split('\n'))  # Separate by line
        for line in license_plate_lines:
            line = line.split(' ')
            line[0] = str(classes.index(line[0]))
            line = ' '.join(line)
            f.write(line + '\n')

# Generate obj.names
print("Writing obj.names ...")
with open('obj.names', 'w') as f:
    for c in classes:
        f.write(CLASSES_REVERSED[int(c)] + '\n')
