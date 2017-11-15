from random import choice, randrange, uniform

from os import listdir

from PIL import Image, ImageDraw, ImageFont

class ImageGenerator():

	data_dir = "data"
	plate_filepath = "{0}/generated_plates".format(data_dir)
	sample_image_filepath = "{0}/sample_images".format(data_dir)
	result_dir = "{0}/dataset".format(data_dir)
	images_paths = list()
	plates_paths = list()


	def get_image(self, name):

		base = Image.open(self.sample_image_filepath+"/"+name).convert('RGBA')

		return base

	def get_plate(self, name):

		base = Image.open(self.plate_filepath+"/"+name).convert('RGBA')

		return base

	def explore_directories(self):

		# Get images
		self.images_paths = listdir(self.sample_image_filepath)

		# Get plates
		self.plates_paths = [file for file in listdir(self.plate_filepath) if file.endswith('.png')]

	def save_bounding_boxes(self, image_n, plate_n, offset, plate_d, image_d):

		txt_name = plate_n.replace("png", "txt")
		txt_file = open(self.plate_filepath+"/"+txt_name,"r")

		new_txt = open(self.result_dir+"/"+image_n+txt_name,"w")

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
			new_center_x = (x0+x1)/2.0/image_d[0]
			new_center_y = (y0+y1)/2.0/image_d[1]
			new_width = (x1-x0)*1.0/image_d[0]
			new_height = (y1-y0)*1.0/image_d[1]

			new_line = "{0} {1} {2} {3} {4}\n".format(yolo_class,
            										   new_center_x,
            										   new_center_y,
            										   new_width,
            										   new_height)

			print(new_line)
			new_txt.write(new_line)
		txt_file.close()
		new_txt.close()


	def make_images(self, plates_by_image=1, repeat=True, min_image_percentage=0.1,max_image_percentage=0.3, allow_crop=False):

		# Get directories
		self.explore_directories()

		if(len(self.plates_paths)/plates_by_image < len(self.images_paths)):
			print(" Repeating plates because : more images than ",plates_by_image,"plates by image")
			repeat = True


		# Start combinations
		for image_name in self.images_paths:

			image = self.get_image(image_name)
			im_width, im_height = image.size

			# Get plates
			plate_names = list()
			for i in range(plates_by_image):

				plate_names.append(choice(self.plates_paths))
				if not repeat:
					self.plates_paths.remove(plate_names[i])

			# New base_name
			new_image_name = image_name[:image_name.find(".")]+"_plates_"

			# Put plates over the other
			for plate_name in plate_names:

				plate = self.get_plate(plate_name)

				pt_width, pt_height = plate.size

				# Calculate new dimensions
				image_percentage = uniform(min_image_percentage,max_image_percentage)
				print(image_percentage)

				basewidth = int(im_width*image_percentage)
				wpercent = (basewidth/float(pt_width))
				hsize = int((float(pt_height)*float(wpercent)))

				# New dimensions
				plate = plate.resize((basewidth,hsize), Image.ANTIALIAS)
				pt_width, pt_height = plate.size

				# New coords

				offset = (0,0)
				if(allow_crop):
					offset = (randrange(-pt_width,im_width),randrange(-pt_height,im_height))
				else:
					offset = (randrange(0,im_width-pt_width),randrange(0,im_height-pt_height))

				image.paste(plate, offset, plate)

				# Modify bounding boxes
				self.save_bounding_boxes(new_image_name,plate_name,offset,(pt_width,pt_height),(im_width,im_height))

			image.save(self.result_dir+"/"+new_image_name+plate_name[:plate_name.find(".")]+".png","PNG")

ig = ImageGenerator()
ig.make_images(1, False, 0.1, 0.5, False)