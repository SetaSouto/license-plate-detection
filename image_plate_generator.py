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

	def save_bounding_boxes(self, name):

		txt_name = name.replace("png", "txt")
		txt_file = open(self.plate_filepath+"/"+txt_name)

		

		print("dummy")


	def make_images(self, plates_by_image=1, repeat=True, min_image_percentage=0.1,max_image_percentage=0.3, allow_crop=False):

		# Get directories
		self.explore_directories()

		if(len(self.plates_paths)/plates_by_image < len(self.images_paths)):
			print(" Repeating plates because : more images than plates")
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
				#self.save_bounding_boxes(image_name,plate_name,offset,(pt_width,pt_height),(im_width,im_height))

			image.save(self.result_dir+"/"+
				image_name[:len(image_name)]+
				"_plates_"+str(plates_by_image)+".png","PNG")

ig = ImageGenerator()
ig.make_images(2, False, 0.1, 0.3, False)