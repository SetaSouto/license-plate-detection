from PIL import Image, ImageDraw, ImageFont

# CONFIG VARS
font_filepath = "data/font/cargoplaindemo.ttf"
font_size = 300
plate_filepath = "data/base_plate/plate_without_background.png"
letters = "A"
numbers = "1"

# Get the image
base = Image.open(plate_filepath).convert('RGBA')

# Make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

# Get the font
font = ImageFont.truetype(font_filepath, font_size)
# Get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
for l1 in letters:
    for l2 in letters:
        for l3 in letters:
            for l4 in letters:
                for n1 in numbers:
                    for n2 in numbers:
                        d.text((100, 15), l1 + l2, font=font, fill=(0, 0, 0, 255))
                        d.text((500, 15), l3 + l4, font=font, fill=(0, 0, 0, 255))
                        d.text((950, 15), n1 + n2, font=font, fill=(0, 0, 0, 255))

                        out = Image.alpha_composite(base, txt)

                        out.show()
                        break
