from PIL import Image, ImageDraw, ImageFont
from random import choice


class PlateGenerator():
    # CONFIG VARS
    data_dir = "data"

    font_filepath = "{0}/font/EuroPlate.ttf".format(data_dir)
    font_size = 325

    plate_filepath = "{0}/base_plate/plate_without_background.png".format(data_dir)

    result_dir = "{0}/generated_plates".format(data_dir)

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "1234567890"

    def get_chars(self):
        """
        Returns a tuple with 4 letters and 2 numbers randomly selected.
        """
        return choice(self.letters), choice(self.letters), choice(self.letters), choice(self.letters), choice(
            self.numbers), choice(self.numbers)

    def generate_plate(self, l1, l2, l3, l4, n1, n2, show_bounding_box=False, show=False, save=True):
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
            x_offset = 5
            y_offset = 10
            width = 170
            height = 255
            for x, y, _ in coordinates_and_chars:
                draw.rectangle([x + x_offset, y + y_offset, x + width, y + height], outline="black")

        out = Image.alpha_composite(base, txt)

        if show: out.show()

        if save: out.save("{0}/{1}".format(self.result_dir, l1 + l2 + l3 + l4 + n1 + n2 + ".png"), "PNG")

    def generate_random_plates(self, n, show_bounding_box=False, show=False, save=True):
        """
        Generates n license plates randomly.
        """
        for _ in range(n):
            l1, l2, l3, l4, n1, n2 = self.get_chars()
            self.generate_plate(l1, l2, l3, l4, n1, n2, show_bounding_box=show_bounding_box, show=show, save=save)


# ----- MAIN SCRIPT ----- #
PlateGenerator().generate_random_plates(1, show_bounding_box=True, show=True, save=False)
