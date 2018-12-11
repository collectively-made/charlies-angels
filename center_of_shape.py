# import the necessary packages
import argparse
import imutils
import cv2
import numpy
import math
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())
 
# load the image, convert it to grayscale, blur it slightly,
# and threshold it
im = cv2.imread(args["image"])
imsize = im.size
print(imsize)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
imgray = cv2.blur(imgray,(15,15))
ret,thresh = cv2.threshold(imgray,math.floor(numpy.average(imgray)),255,cv2.THRESH_BINARY_INV)
dilated=cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10)))
_,contours,_ = cv2.findContours(dilated,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

new_contours=[]
for c in contours:
    if cv2.contourArea(c) > 500:
      if cv2.contourArea(c) < 5000:
        new_contours.append(c)
        
best_box=[-1,-1,-1,-1]
for c in new_contours:
  x,y,w,h = cv2.boundingRect(c)
  if best_box[0] < 0:
    best_box=[x,y,x+w,y+h]
  else:
    if x<best_box[0]:
      best_box[0]=x
    if y<best_box[1]:
      best_box[1]=y
    if x+w>best_box[2]:
      best_box[2]=x+w
    if y+h>best_box[3]:
      best_box[3]=y+h
  cv2.rectangle(dilated, (best_box[0],best_box[1]), (best_box[2],best_box[3]), (255, 255, 0), 2)

#print(len(cnts))

# resize the output window
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.namedWindow("Thresh", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("Image", 600,600)

# show the image
cv2.imshow("Image", im)
cv2.imshow("Thresh", dilated)
cv2.waitKey(0)