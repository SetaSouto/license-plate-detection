from random import choice

from PIL import Image, ImageDraw, ImageFont

from yolo_categories import CATEGORIES


class PlateGenerator():
    # CONFIG VARS
    data_dir = "data"

    font_filepath = "{0}/font/EuroPlate.ttf".format(data_dir)
    font_size = 325

    plate_filepath = "{0}/base_plate/plate_without_background.png".format(data_dir)

    result_dir = "{0}/generated_plates".format(data_dir)

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "1234567890"

    license_plate_bounding_box = [31, 24, 1330, 464]

    def get_chars(self):
        """
        Returns a tuple with 4 letters and 2 numbers randomly selected.
        """
        return choice(self.letters), choice(self.letters), choice(self.letters), choice(self.letters), choice(
            self.numbers), choice(self.numbers)

    def generate_plate(self, l1, l2, l3, l4, n1, n2, show_bounding_box=False, show=False, save=True,
                       debug_bounding_box_normalized=False):
        """
        Given 4 letters and 2 numbers generate a license plate.
        Saves the image as a PNG in the results dir.
        """
        # Get the image
        base = Image.open(self.plate_filepath).convert('RGBA')
        # Make a blank image for the text, initialized to transparent text color
        txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
        # Get the font
        font = ImageFont.truetype(self.font_filepath, self.font_size)
        # Get a drawing context
        draw = ImageDraw.Draw(txt)
        # Draw chars
        coordinates_and_chars = [(90, 60, l1),
                                 (270, 60, l2),
                                 (500, 60, l3),
                                 (680, 60, l4),
                                 (940, 60, n1),
                                 (1100, 60, n2)]
        for x, y, c in coordinates_and_chars:
            draw.text((x, y), c, font=font, fill=(0, 0, 0, 255))

        if show_bounding_box:
            for x, y, _ in coordinates_and_chars:
                draw.rectangle(self.get_bounding_box(x, y), outline="black")
                draw.rectangle(self.license_plate_bounding_box, outline="black")

        if debug_bounding_box_normalized:
            for x, y, _ in coordinates_and_chars:
                center_x, center_y, width, height = self.get_bounding_box_normalized(x, y, base.size)
                x0 = (center_x - width / 2) * base.size[0]
                x1 = (center_x + width / 2) * base.size[0]
                y0 = (center_y - height / 2) * base.size[1]
                y1 = (center_y + height / 2) * base.size[1]
                draw.rectangle([x0, y0, x1, y1], outline="black")

        out = Image.alpha_composite(base, txt)

        if show: out.show()

        if save:
            out.save("{0}/{1}".format(self.result_dir, l1 + l2 + l3 + l4 + n1 + n2 + ".png"), "PNG")
            self.save_label(coordinates_and_chars, out.size)

    def generate_random_plates(self, n, show_bounding_box=False, show=False, save=True,
                               debug_bounding_box_normalized=False):
        """
        Generates n license plates randomly.
        """
        for index in range(n):
            l1, l2, l3, l4, n1, n2 = self.get_chars()
            self.generate_plate(l1, l2, l3, l4, n1, n2, show_bounding_box=show_bounding_box, show=show, save=save,
                                debug_bounding_box_normalized=debug_bounding_box_normalized)
            print("Generated plates: ", index)

    def save_label(self, coordinates_and_chars, image_size):
        """
        Receives the tuples with the x left, y top and char a
        :param coordinates_and_chars: List of tuples as (int, int, char).
        :param image_size: Tuple as (width, height)
        """

        def get_string(x, y, c):
            """
            Given a position (x left, y top) and a char returns the string to write as a YOLO format:
            "category center_x center_y width height"
            """
            center_x, center_y, width, height = self.get_bounding_box_normalized(x, y, image_size)
            category = CATEGORIES[c]
            return "{0} {1} {2} {3} {4}\n".format(category, center_x, center_y, width, height)

        labels = self.result_dir + "/" + "".join([tuple[2] for tuple in coordinates_and_chars]) + ".txt"
        with open(labels, "w") as f:
            # Save chars bounding boxes
            for x, y, c in coordinates_and_chars:
                f.write(get_string(x, y, c))
            # Append bounding box for entire license plate
            category = CATEGORIES["LICENSE-PLATE"]
            center_x, center_y, width, height = self.normalize_bounding_box(self.license_plate_bounding_box,
                                                                            image_size)
            f.write("{0} {1} {2} {3} {4}".format(category,
                                                 center_x,
                                                 center_y,
                                                 width,
                                                 height))

    def get_bounding_box(self, x, y):
        """
        Returns the bounding box coordinates for a letter with a position given where x is the left side and y is the
        top side.
        Returns [x left, y top, x right, y bottom]
        """
        x_offset = 5
        y_offset = 10
        width = 170
        height = 255

        return [x + x_offset, y + y_offset, x + width, y + height]

    def get_bounding_box_normalized(self, x, y, image_size):
        """
        Normalize the bounding box because YOLO understands the bounding box in percentages of the full image.
        """
        # Get bounding box
        bounding_box = self.get_bounding_box(x, y)
        return self.normalize_bounding_box(bounding_box, image_size)

    def normalize_bounding_box(self, bounding_box, image_size):
        # Get parameters
        width = bounding_box[2] - bounding_box[0]
        center_x = bounding_box[0] + (width / 2)
        height = bounding_box[3] - bounding_box[1]
        center_y = bounding_box[1] + (height / 2)
        # Relative to image size
        width /= image_size[0]
        height /= image_size[1]
        center_x /= image_size[0]
        center_y /= image_size[1]

        return center_x, center_y, width, height


# ----- MAIN SCRIPT ----- #
PlateGenerator().generate_random_plates(2000,
                                        show_bounding_box=False,
                                        show=False,
                                        save=True,
                                        debug_bounding_box_normalized=False)
