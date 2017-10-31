import matplotlib.pyplot as plt
import matplotlib.image as mpimage
import numpy as np
from skimage import transform as tf


def transform(image):
    """
    Receives a clean generated license plate image and transform it randomly.
    :param image: Clean generated image with PlateGenerator.
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
    return tf.warp(image, transformation, output_shape=image.shape)

image = mpimage.imread("data/generated_plates/GXYF08.png")
warped = transform(image)
plt.imshow(warped)
plt.show()