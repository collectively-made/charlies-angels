# import the necessary packages
import argparse
import imutils
import cv2
import numpy
import math
 
# construct the argument parser and parse the cmd line imput arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="path to the input image")
#args = vars(ap.parse_args())
 
# load the image
#im = cv2.imread(args["image"])
im = cv2.imread("scan1.jpeg")

# convert it to grayscale
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

# remove very dark/light pixels (set to black)
# this didn't help :_(
#newimage = imgray.copy()
#for i in range(len(imgray)):
#    for j in range(len(imgray[i])):
#        if imgray[i,j] >= 230:
#          newimage[i,j] = 0
#        elif imgray[i,j] <= 50:
#          newimage[i,j] = 0

# blur it slightly
#imgrayblur = cv2.blur(imgray,(25,25))
#imgrayblur = cv2.GaussianBlur(imgray,(5,5),0)

# remove noise - see docs for inefficiencies
#imgrayfiltered = cv2.bilateralFilter(imgray, 18, 150, 150)

# another method to clean up noise
#window = numpy.ones((5,5), numpy.uint8)
#imgrayeroded = cv2.erode(imgray, window, iterations = 1)

# threshold it; returns a binary (black/white) based on threshold number
ret0,thresh0 = cv2.threshold(imgray,70,255,cv2.THRESH_BINARY_INV)

# more advanced thresholding
#thresh = cv2.adaptiveThreshold(thresh0,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
#ret,thresh = cv2.threshold(imgrayblur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# ???
#dilated = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10)))

# returns an array of all the blobs (contours) it found
#contours=[]
_,contours,_ = cv2.findContours(thresh0,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


# filter out blobs that don't meet certain size (area) criteria
# might use area of bounding rect instead
new_contours=[]
for c in contours:
  if cv2.contourArea(c) > ((im.size * 1) // 1000): # => 0.1% of size
    if cv2.contourArea(c) < (im.size // 9): # => max 9 photos fit
      new_contours.append(c)
      print("blob size c: ", cv2.contourArea(c))

final_contours = []

# draw the blobs bounding rectangle on original image
for c in new_contours:
  # draw axis-aligned bounding box
  
  x,y,w,h = cv2.boundingRect(c)
  cv2.rectangle(im, (x,y), (x+w, y+h), (255,255,0), 3)
  final_contours.append((x,y,w,h))

  # draw contour-aligned bounding box
  #contourbox = cv2.minAreaRect(c)
  #corners = numpy.int0(cv2.boxPoints(contourbox)) #int0->intp
  #cv2.drawContours(im, [corners], 0, (0,0,255), 3)

print(final_contours)

# ALL THE THINGS THAT WILL DISPLAY

# stats to display for analysis
print("Image Size: ", im.size) #image size in pixels; for use in future
print("Min Blob Size: ", ((im.size * 1) // 1000), "Max: ", (im.size // 9))
print("Blobs: ", len(contours)) #total number of blobs found
print("Filtered Blobs: ", len(new_contours)) #total number of blobs after size filter

# create display windows
#cv2.namedWindow("Im", cv2.WINDOW_NORMAL)
#cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
#cv2.namedWindow("Eroded", cv2.WINDOW_NORMAL)
cv2.namedWindow("Thresh", cv2.WINDOW_NORMAL)
#cv2.namedWindow("Blur", cv2.WINDOW_NORMAL)

#resize the output windows bc on a PC...well, its a PC
#cv2.resizeWindow("Im", 600,600)
#cv2.resizeWindow("Image", 600,600)
#cv2.resizeWindow("Eroded", 600,600)
cv2.resizeWindow("Thresh", 600,600)
#cv2.resizeWindow("Blur", 600,600)

# show the image
#cv2.imshow("Im", im)
#cv2.imshow("Image", newimage)
#cv2.imshow("Eroded", thresh0)
cv2.imshow("Thresh", im)
#cv2.imshow("Blur", imgrayblur)


cv2.waitKey(0)