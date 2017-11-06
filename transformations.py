import matplotlib.pyplot as plt
import matplotlib.image as mpimage
import numpy as np
from PIL import Image
from skimage import transform as tf


def transform(image,bb_file):
    """
    Receives a clean generated license plate image and transform it randomly.
    :param image: Clean generated image with PlateGenerator.
    :param bb_file: Bounding Boxes coordinates filepath.
    :return: A transformed image as an ndarray.
    """
    source_points = np.array([[30, 24],
                              [43, 458],
                              [1314, 461],
                              [1327, 24]])
    destination_points = np.array([[30, 24],
                                   [60, 500],
                                   [1060, 350],
                                   [1000, 0]])
    transformation = tf.ProjectiveTransform()
    transformation.estimate(destination_points, source_points)

    get_new_bounding_boxes(len(image[0]),len(image),bb_file,transformation.params,destination_points)

    return tf.warp(image, transformation, output_shape=image.shape)

def get_new_bounding_boxes(width,height,bb_file,transf,dest_points):
    """
    Receives an image coordinates and the YOLO formatted file to transform
    the bounding boxes
    :param width: the image width.
    :param height: the image height.
    :param bb_file: the bounding box filepath.
    :param transf: the transformation listin numpy format.
    """

    # Read file and get the coordinates
    coordinates = list(open(bb_file,"r"))
    for i in range(len(coordinates)):
      parsed_line = coordinates[i].split(" ")
      parsed_line[0] = int(parsed_line[0])
      for j in range(1,5):
        parsed_line[j] = float(parsed_line[j])
      coordinates[i] = parsed_line

    # Get point coordinates
    new_coords = list()

    # plate label coordinates

    """
    image_dims = [(dest_points[0][0]+dest_points[1][0]+dest_points[2][0]+dest_points[3][0])/4,
                  (dest_points[0][1]+dest_points[1][1]+dest_points[2][1]+dest_points[3][1])/4]
    image_center = 
    """
    # SECTION HARCODEADA
    image_dims = np.dot([width, height, 1],transf)[:2] # new dimensions
    image_dims = 1.3*image_dims
    """
    print(image_dims)
    print(image_dims)
    """
    for i in range(7):
      #print("==========================================")
      this_class = list()

      # Pixel values
      center_x = coordinates[i][1]*width
      center_y = coordinates[i][2]*height
      box_w = coordinates[i][3]*width/2 # half value
      box_h = coordinates[i][4]*height/2  # half value

      # Points
      top_left_p = [center_x-box_w,center_y+box_h,1]
      bottom_left_p = [center_x-box_w,center_y-box_h,1]
      top_right_p = [center_x+box_w,center_y+box_h,1]
      bottom_right_p = [center_x+box_w,center_y-box_h,1]
      #print(top_left_p,bottom_left_p,top_right_p,bottom_right_p)

      # Transform
      top_left_p = np.dot(top_left_p,transf)
      bottom_left_p = np.dot(bottom_left_p,transf)
      top_right_p = np.dot(top_right_p,transf)
      bottom_right_p = np.dot(bottom_right_p,transf)
      #print(top_left_p,bottom_left_p,top_right_p,bottom_right_p)

      # Append new values in ratios
      this_class.append(coordinates[i][0]) #class
      this_class.append(abs(top_left_p[0]+top_right_p[0]+bottom_left_p[0]+bottom_right_p[0])/4/image_dims[0]) # new center x
      this_class.append(abs(top_left_p[1]+bottom_left_p[1]+top_right_p[1]+bottom_right_p[1])/4/image_dims[1]) # new center y
      this_class.append(abs(top_left_p[0]-top_right_p[0]+bottom_left_p[0]-bottom_right_p[0])/2/image_dims[0]) # new width
      this_class.append(abs(top_left_p[1]-bottom_left_p[1]+top_right_p[1]-bottom_right_p[1])/2/image_dims[1]) # new height

      # Save this result
      new_coords.append(this_class)

    f = open("AUTE25_t.txt","w")
    for values in new_coords:
      print(values)
      f.write(str(values[0])+" "+
              str(values[1])+" "+
              str(values[2])+" "+
              str(values[3])+" "+
              str(values[4])+"\n")


image = mpimage.imread("data/generated_plates/AUTE25.png")
warped = transform(image,"data/generated_plates/AUTE25.txt")
plt.imshow(warped)
plt.show()
#new_image = Image.fromarray(warped).convert('RGB')
#new_image.save("AUTE25_t.png", "PNG")
mpimage.imsave("AUTE25_t.png",warped)