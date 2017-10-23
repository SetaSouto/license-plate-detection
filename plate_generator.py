from PIL import Image, ImageDraw, ImageFont

# CONFIG VARS
font_filepath = "data/font/cargoplaindemo.ttf"
font_size = 80
plate_filepath = "data/base_plate/plate_without_background.png"

# Get the image
base = Image.open(plate_filepath).convert('RGBA')

# Make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

# Get the font
font = ImageFont.truetype(font_filepath, font_size)
# Get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
d.text((100, 100), "BB", font=font, fill=(0, 0, 0, 255))

out = Image.alpha_composite(base, txt)

out.show()
