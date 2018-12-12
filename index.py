# import the necessary packages
import argparse
import imutils
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())
 
# load the image, convert it to grayscale, blur it slightly,
# and threshold it
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]


# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)


# try to find the right size bounding boxes and draw them
new_cnts=[]
for c in cnts:
    if cv2.contourArea(c) > 0:
      if cv2.contourArea(c) < 1009800:
        new_cnts.append(c)

best_box=[-1,-1,-1,-1]
for c in new_cnts:
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
  cv2.rectangle(image, (x,y), (x+w, y+h), (255, 255, 0), 2)

print(len(cnts))
print(len(new_cnts))

# loop over the contours
for c in cnts:
 
	 # draw the contour and center of the shape on the image
  cv2.drawContours(image, [c], -1, (0, 255, 0), 2)


# resize the output window
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.namedWindow("Thresh", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("Image", 600,600)

# show the image
cv2.imshow("Image", image)
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)