# import the necessary packages
from __future__ import print_function
import numpy
import argparse
import cv2
import imutils
import os

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="path to input image")
#args = vars(ap.parse_args())

# load the original image
#original = cv2.imread(args["image"])
original = cv2.imread("scan1.jpeg")

# adjust gamma
def adjust_gamma(image, gamma = 1.0):
  # build a lookup table mapping the pixel values [0, 255] to
  # their adjusted gamma values
  invGamma = 1.0 / gamma
  table = numpy.array([((i / 255.0) ** invGamma) * 255 for i in numpy.arange(0, 256)]).astype("uint8")

  # apply gamma correction using the lookup table
  return cv2.LUT(image, table)

# loop over various values of gamma
for index, gamma in enumerate(numpy.arange(.1, 1.1, 0.2)):
  # ignore when gamma is 1 (there will be no change to the image)
  if gamma == 1:
    continue

  # apply gamma correction and show the images
  gamma = gamma if gamma > 0 else 0.1
  
  # return image with adjusted gamma
  adjusted = adjust_gamma(original, gamma = gamma)
  
  # add text on adjusted image for imshow
  #cv2.putText(adjusted, "g={}".format(gamma), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 12, (0, 0, 255), 3, bottomLeftOrigin = 1)
  
  # write images to a file
  path = 'C:\\Users\\Bo\\Projects\\charlies-angels\\gammaimages'
  cv2.imwrite(os.path.join(path , 'image_gamma_' + str(index) + '.png'), adjusted)
  
  # display image
  #cv2.namedWindow("Images", cv2.WINDOW_NORMAL)
  #cv2.resizeWindow("Images", 1200, 600)
  #cv2.imshow("Images", numpy.hstack([original, adjusted]))
  #cv2.waitKey(0)