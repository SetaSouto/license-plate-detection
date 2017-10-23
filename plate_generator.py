from PIL import Image, ImageDraw, ImageFont

# CONFIG VARS
data_dir = "data"

font_filepath = "{0}/font/EuroPlate.ttf".format(data_dir)
font_size = 325

plate_filepath = "{0}/base_plate/plate_without_background.png".format(data_dir)

result_dir = "{0}/generated_plates".format(data_dir)

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"

# draw text, half opacity
for l1 in letters:
    for l2 in letters:
        for l3 in letters:
            for l4 in letters:
                for n1 in numbers:
                    for n2 in numbers:
                        # Get the image
                        base = Image.open(plate_filepath).convert('RGBA')

                        # Make a blank image for the text, initialized to transparent text color
                        txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

                        # Get the font
                        font = ImageFont.truetype(font_filepath, font_size)
                        # Get a drawing context
                        d = ImageDraw.Draw(txt)
                        d.text((100, 60), l1 + l2, font=font, fill=(0, 0, 0, 255))
                        d.text((500, 60), l3 + l4, font=font, fill=(0, 0, 0, 255))
                        d.text((950, 60), n1 + n2, font=font, fill=(0, 0, 0, 255))

                        out = Image.alpha_composite(base, txt)

                        out.save("{0}/{1}".format(result_dir, l1 + l2 + l3 + l4 + n1 + n2 + ".png"), "PNG")
