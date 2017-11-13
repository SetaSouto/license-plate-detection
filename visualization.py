import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw


def show_image_with_coords(src):
    """
    Show a given image with coordinates that you can use with your mouse and view the position of a pixel.
    :param src: Source path.
    """
    img = mpimg.imread(src)
    plt.imshow(img)
    plt.show()


def show_image_with_bounding_boxes(src):
    """
    Select a given image source and its labels and show the bounding boxes.
    :param src: Source path.
    """

    def get_data():
        if src[-3:] == "png":
            labels_file = src[:-3] + "txt"
            with open(labels_file) as f:
                return list(filter(lambda x: len(x) > 0,
                                   [list(map(float, line.split(" ")[1:])) for line in f.read().split("\n")]))
        else:
            raise AssertionError("File not supported. Extension: " + src.plit(".")[-1])

    def transform_data(data):
        result = []
        for center_x, center_y, width, height in data:
            x0 = (center_x - width / 2) * base.size[0]
            x1 = (center_x + width / 2) * base.size[0]
            y0 = (center_y - height / 2) * base.size[1]
            y1 = (center_y + height / 2) * base.size[1]
            result.append((x0, x1, y0, y1))
        return result

    base = Image.open(src).convert('RGBA')
    # Make a blank image for the rectangles
    rectangles_image = Image.new('RGBA', base.size, (255, 255, 255, 0))
    # Get a drawing context
    draw = ImageDraw.Draw(rectangles_image)
    # Draw rectangles
    for x0, x1, y0, y1 in transform_data(get_data()):
        draw.rectangle([x0, y0, x1, y1], outline="black")
    out = Image.alpha_composite(base, rectangles_image)
    out.show()


# ----- MAIN SCRIPT ----- #
show_image_with_bounding_boxes("data/generated_plates/GXYF08.png")
