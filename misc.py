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
thresh = cv2.threshold(blurred, 55, 255, cv2.THRESH_BINARY)[1]


# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the contours
for c in cnts:
  # draw the bounding rectangle
  x, y, w, h = cv2.boundingRect(c)
  cv2.rectangle(image, (x,y), (x+w, y+h), (255, 255, 0), 2)
  
  # Label each bounding rectangle found
  cv2.putText(image, "Tagged", (x+int(w/2), y+int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
  
  # draw the contour and center of the shape on the image
  cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

print(len(cnts))

# resize the output window
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.namedWindow("Thresh", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("Image", 600,600)

# show the image
cv2.imshow("Image", image)
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)