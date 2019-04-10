import cv2
import numpy
from matplotlib import pyplot as plt
import argparse
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# load the image
img = cv2.imread(args["image"], 0)

# save the grayscale image to this path
path = 'C:\\Users\\Bo\\Projects\\charlies-angels\\gammaimages'
cv2.imwrite(os.path.join(path, 'image_grayscale.png'), img)


# plot the histogram
plt.hist(img.ravel(),256,[0,80])
plt.show()