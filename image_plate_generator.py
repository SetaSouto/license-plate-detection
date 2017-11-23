from os import listdir
from random import choice, randrange, uniform

from PIL import Image
import datetime 

class ImageGenerator():
    data_dir = "data"
    plate_filepath = "{0}/generated_plates".format(data_dir)
    sample_image_filepath = "{0}/sample_images".format(data_dir)
    result_dir = "{0}/dataset".format(data_dir)
    images_paths = list()
    plates_paths = list()
    used_space = list()
    overlapping_delta = 0.01

    def get_image(self, name):

        base = Image.open(self.sample_image_filepath + "/" + name).convert('RGBA')

        return base

    def get_plate(self, name):

        base = Image.open(self.plate_filepath + "/" + name).convert('RGBA')

        return base

    def explore_directories(self):
        """
        Look up files in the directories defined in the class
        """

        # Get images
        self.images_paths = listdir(self.sample_image_filepath)

        # Get plates
        self.plates_paths = [file for file in listdir(self.plate_filepath) if file.endswith('.png')]

    def save_bounding_boxes(self, plate_n, offset, plate_d, image_d, text_file):
        """
        Given a plate's name recalculate the relative position and dimensions and
        save them on a text_file
        :param plate_n: plate's name
        :param offset: the plate's position offset on the image
        :param plate_d: plate's dimensions
        :param image_d: new image dimensions
        :param text_file: output file
        """

        txt_name = plate_n.replace("png", "txt")
        txt_file = open(self.plate_filepath + "/" + txt_name, "r")

        for line in txt_file:
            yolo_class, center_x, center_y, width, height = line.split(" ")
            center_x = float(center_x)
            center_y = float(center_y)
            width = float(width)
            height = float(height)
            # Get coordinates
            x0 = (center_x - width / 2) * plate_d[0] + offset[0]
            x1 = (center_x + width / 2) * plate_d[0] + offset[0]
            y0 = (center_y - height / 2) * plate_d[1] + offset[1]
            y1 = (center_y + height / 2) * plate_d[1] + offset[1]
            # Get new percentages
            new_center_x = (x0 + x1) / 2.0 / image_d[0]
            new_center_y = (y0 + y1) / 2.0 / image_d[1]
            new_width = (x1 - x0) * 1.0 / image_d[0]
            new_height = (y1 - y0) * 1.0 / image_d[1]

            new_line = "{0} {1} {2} {3} {4}\n".format(yolo_class,
                                                      new_center_x,
                                                      new_center_y,
                                                      new_width,
                                                      new_height)
            text_file.write(new_line)

        txt_file.close()

    def position_is_occupied(self, offset, plate_d):
        """
        Verifies if we are pasting a plate over another
        """
        # Empty list, then save
        for element in self.used_space:
            if (offset[0] > element[0] and offset[0] < element[2]):
                return True
            if (offset[1] > element[1] and offset[1] < element[3]):
                return True

        # posX, posY, posX+width, posY+height
        self.used_space.append([offset[0], offset[1], offset[0] + plate_d[0], offset[1] + plate_d[1]])
        return False

    def make_images(self, plates_by_image=1, repeat=True, min_image_percentage=0.1, max_image_percentage=0.3,
                    allow_crop=False, paste_over=False):
        """
        For the class given directories paste license plates over each image on the directory.
        :param plates_by_image: number of plates to be pasted on each image.
        :param repeat: if to repeat license plates given a set of images and plates.
        :param min_image_percentage: minimum percentage of the image's width to redimension a plate
        :param max_image_percentage: maximum percentage of the image's width to redimension a plate
        :param allow_crop: if to allow a plate to be pasted in a position that will crop it
        """
        # Get directories
        self.explore_directories()


        if (len(self.plates_paths) / plates_by_image < len(self.images_paths)):
            print(" Repeating plates because : more images than ", plates_by_image, "plates by image")
            repeat = True

        # Start combinations
        counter = 0
        for image_name in self.images_paths:

            image = self.get_image(image_name)
            im_width, im_height = image.size

            # Get plates
            plate_names = list()
            for i in range(plates_by_image):

                plate_names.append(choice(self.plates_paths))
                if not repeat:
                    self.plates_paths.remove(plate_names[i])

            # =============== FILE NAMES =================
            # New base_name
            new_image_name = image_name[:image_name.find(".")] + "_plates_"
        	
            file_name = self.result_dir + "/" + new_image_name + "_plates_" + str(plates_by_image) + "_" +datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            new_txt = open(file_name + ".txt", "w")

            # Dimensions already occupied
            self.used_space = list()

            # Put plates over the other
            for plate_name in plate_names:

                plate = self.get_plate(plate_name)

                pt_width, pt_height = plate.size

                # Calculate new dimensions
                image_percentage = uniform(min_image_percentage, max_image_percentage)

                basewidth = int(im_width * image_percentage)
                wpercent = (basewidth / float(pt_width))
                hsize = int((float(pt_height) * float(wpercent)))

                # New dimensions
                plate = plate.resize((basewidth, hsize), Image.ANTIALIAS)
                pt_width, pt_height = plate.size

                # New coords
                if (paste_over):
                    offset = (0, 0)
                    if (allow_crop):
                        offset = (randrange(-pt_width, im_width), randrange(-pt_height, im_height))
                    else:
                        offset = (randrange(0, im_width - pt_width), randrange(0, im_height - pt_height))

                    image.paste(plate, offset, plate)
                else:
                    # Try to find a suitable spot with some overlapping allowed
                    occupied = True
                    offset = (0, 0)

                    while occupied:
                        if (allow_crop):
                            offset = (randrange(-pt_width, im_width), randrange(-pt_height, im_height))
                        else:
                            offset = (randrange(0, im_width - pt_width), randrange(0, im_height - pt_height))

                        occupied = self.position_is_occupied(offset, (pt_width, pt_height))

                    image.paste(plate, offset, plate)

                # Modify bounding boxes
                self.save_bounding_boxes(plate_name, offset, (pt_width, pt_height), (im_width, im_height), new_txt)

            image = image.convert("RGB")
            image.save(file_name + ".jpg", "JPEG")
            new_txt.close()

            counter += 1
            print("Images generated until now:", counter)


ig = ImageGenerator()
ig.make_images(plates_by_image=2,
               repeat=False,
               min_image_percentage=0.1,
               max_image_percentage=0.4,
               allow_crop=False,
               paste_over=False)
