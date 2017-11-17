import matplotlib.pyplot as plt
import matplotlib.image as mpimage
import numpy as np
from skimage import transform as tf
from PIL import Image, ImageDraw

DEBUG = False

def find_bounding_boxes(image_name,size,transformation):

    txt_name = image_name[:image_name.find(".")]+".txt"
    txt_file = open(txt_name,"r")
    new_txt = open("test1.txt","w")
    print(size)
    # Get coordinates
    i = 0
    for line in txt_file:
      yolo_class, center_x, center_y, width, height = line.split(" ")
      center_x = float(center_x)
      center_y = float(center_y)
      width = float(width)
      height = float(height)
      # Get coordinates
      x0 = (center_x - width / 2) * size[1]
      x1 = (center_x + width / 2) * size[1]
      y0 = (center_y - height / 2) * size[0]
      y1 = (center_y + height / 2) * size[0]
      # Make a rectangle on a new image
      temp = Image.new('RGBA', (size[1],size[0]), (255, 255, 255, 255))
      draw = ImageDraw.Draw(temp)
      draw.rectangle([x0,y0,x1,y1],fill=(0,0,0,255))

      if DEBUG:
        temp.show()
        w = input()

      temp = tf.warp(temp, transformation, output_shape=size, mode='constant', cval=1.0)

      if DEBUG:
        plt.imshow(temp)
        plt.show()
        w = input()

      # Find the new coordinates for p0 and p1
      width = len(temp[0])
      height = len(temp)

      x0 = width
      y0 = height
      x1 = y1 = 0

      compare_point = 0.0#temp[0][0][0]

      for i in range(width):  
        for j in range(height):
          if(temp[j][i][0] == compare_point or temp[j][i][1] ==compare_point or temp[j][i][2] ==compare_point):
            # change max
            if(i<x0):
              x0 = i
            elif(i>x1):
              x1 = i

            if(j<y0):
              y0 = j
            elif(i>y1):
              y1 = j

      print("p1: ",x0,y0," p2: ",x1,y1)
      
      # Get center and width
      center_x = (x0+x1)/2.0/size[1]
      center_y = (y0+y1)/2.0/size[0]
      width = (x1-x0)/size[1]
      height = (y1-y0)/size[0]
      new_txt.write("{0} {1} {2} {3} {4}\n".format(yolo_class,
                                                   center_x,
                                                   center_y,
                                                   width,
                                                   height))

def transform(image_name, source_points, destination_points):
    """
    Receives a clean generated license plate image and transform it randomly.
    :param image: Clean generated image with PlateGenerator.
    :return: A transformed image as an ndarray.
    """
    image = mpimage.imread(image_name)

    transformation = tf.ProjectiveTransform()
    transformation.estimate(destination_points, source_points)

    find_bounding_boxes(image_name,(image.shape[0],image.shape[1]),transformation)

    new_image = tf.warp(image, transformation, output_shape=image.shape)

    new_image = Image.fromarray(new_image)
    
    new_image.save("test1.png","PNG")


original_points = np.array([[30, 24],
                          [43, 458],
                          [1314, 461],
                          [1327, 24]])

transformation_points = np.array([[30, 24],
                                   [60, 500],
                                   [1060, 350],
                                   [1000, 0]])

warped_image = transform("data/generated_plates/AUTE25.png",original_points,transformation_points)
plt.imshow(warped_image)
plt.show()