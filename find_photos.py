# import the necessary packages
import argparse
import imutils
import cv2
import numpy
import math
from toolz import pipe
 
# construct the argument parser and parse the cmd line imput arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="path to the input image")
#args = vars(ap.parse_args())

# load the image
#im = cv2.imread(args["image"])
#im = cv2.imread("./gammaimages/image_gamma_4.png")
im = cv2.imread("scan1.jpeg")

# get image pixel size (coerce to integer)
imagesize = im.size * 1

# user defined inputs (more to come...)
#1 image listing suggests all are same size
#might guess list of sizes and ask user to add or delete from guess list
#images sizes is also a factor for aspect ratios...
imageSizes = []
minImageSize = (imagesize // 1000) # => 0.1% of total; '//' is floor division
maxImageSize = (imagesize // 9) # => max 9 photos fit; '//' is floor division
aspectRatios = [(1,1),(7,6),(5,4),(17,13),(4,3),(7,5),(3,2),(30,17),(16,9)]

def ratioToFraction(ratio):
  return max(ratio[0],ratio[1]) / min(ratio[0],ratio[1])

aspectFractions = map(ratioToFraction, aspectRatios)

def includeFraction(ratio):
  return {"ratio": ratio, "fraction": ratioToFraction(ratio)}

aspects = map(includeFraction, aspectRatios)

print("\n User Defined Inputs...")
print("Min Image Size: ", minImageSize)
print("Max Image Size: ", maxImageSize)

# Image stats
print("\n Analysis Stats...")
print("Image Size: ", imagesize) #image size in pixels; for use in future


# convert image to grayscale
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

# creates black/white image based on threshold grey value
binary = cv2.THRESH_BINARY
#thresh = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_MEAN_C,binary,111,2)
#thresh = cv2.adaptiveThreshold(imfilter,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,binary,311,2)
ret,thresh = cv2.threshold(imgray,70,255,binary)

# removing noise
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
#dilated = cv2.morphologyEx(imgray, cv2.MORPH_OPEN, kernal)
#dilated = cv2.morphologyEx(imgray, cv2.MORPH_CLOSE, kernel)

#threshblur = cv2.GaussianBlur(thresh,(5,5),0)


# set this as the image to run analayis on
imageforanalysis = thresh
#set this as the image to draw results on and show
imageforviewing = im

# returns an array of all the blobs (contours) it found
#contours=[]
_,contours,_ = cv2.findContours(imageforanalysis,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
print("Initial Contour Count: ", len(contours)) #total number of blobs found

# select contours of certain size (area)
def limitSizes(contours):
  print(len(contours))
  limited_size_contours=[]
  for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)
    area = w * h
    if area > minImageSize:
      if area < maxImageSize:
        limited_size_contours.append(contour)
        #print("limited sized contour area: ", area)
  print("Size-Limited Contours: ", len(limited_size_contours))
  return limited_size_contours

# convert a list of contours into a list of their bounding boxes
def mapContoursToBoxes(contours):
  contourmap = list(map(cv2.boundingRect,contours))
  #print("contourmap: ", contourmap)
  print("Count of mapContoursToBoxes: ", len(contourmap))
  return contourmap

# find similar/engulfed bounding boxes
def findSubboxes(boundingboxes):
  similarboxes = []
  
  # assume a box...
  for box in boundingboxes:
    x2 = box[0]
    y2 = box[1]
    w2 = box[2]
    h2 = box[3]
    # if otherbox is within box add to similarboxes
    for otherbox in boundingboxes:
      x1 = otherbox[0]
      y1 = otherbox[1]
      w1 = otherbox[2]
      h1 = otherbox[3]
      if x1>x2 and y1>y2 and (x1+w1)<(x2+w2) and (y1+h1)<(y2+h2):
      #if x1 > x2:
        similarboxes.append(otherbox)
      #else:
        #print("x1: ", x1)
        #print("x2: ", x2)
  #print("similar boxes: ", similarboxes)
  subboxes = set(similarboxes)
  
  print("Count of similar boxes: ", len(similarboxes))
  print("Count of subboxes (unique similar boxes): ", len(subboxes))
  
  return list(subboxes)

# 'set' serves as a convenient way to get the unique values of a list
# Sc ⋂ B: given Subboxes as S and Boundingboxes as B,
# set math yields the intersection of what is not in S (S complement) and B
def removeSubboxes(boundingboxes):
  boxes = set(boundingboxes)-set(findSubboxes(boundingboxes))
  return list(boxes)

# convert bounding boxes to user defined aspect ratios
def mapBoxesToAspectRatio(boundingboxes):
  #what if box is slightly larger than aspect ratio???
  
  for box in boundingboxes:
    xCoord = box[0]
    yCoord = box[1]
    width = box[2]
    height = box[3]
    
    
    def getStats(width,height):
      if max(width,height) == width:
        longSideAxis = "x"
        longSideLength = width
        shortSideAxis = "y"
        shortSideLength = height
      else:
        longSideAxis = "y"
        longSideLength = height
        shortSideAxis = "x"
        shortSideLength = width
        
      aspectFraction = longSideLength / shortSideLength
      return {
        "longSideAxis": longSideAxis,
        "longSideLength": longSideLength,
        "shortSideAxis": shortSideAxis,
        "shortSideLength": shortSideLength,
        "aspectFraction": aspectFraction
      }
      
    
    def calculateClosestAspect(boxStats,aspects):
      
      # map won't garauntee the resulting list is in same order; use for loop
      diffs = []
      for aspect in aspects:
        diffs.append(abs(boxStats["aspectFraction"]-aspect["fraction"]))
      
      # use index of smallest diff to select from aspect fractions list
      closestAspect = aspects[diffs.index(min(diffs))]
      
      return closestAspect
    
    def guessTransformParameters:
      
      def chooseTransformAxis(boxStats, aspect):
        #calculate delta to coerce longSide into closestAspectRatio
        #calculate delta to coerce shortSide into closestAspectRatio
        #one side multiplied by the aspect ratio yields the needed other side value
          #be sure to check both adding and subtracting sides to coerce
        #select the min of the of the absValue of the 4 resulting values
        #actually maybe just use values that grow boxes rather than shrink boxes
        #but what if box is only slightly larger than aspect ratio; should shrink box?
        #it turns out that increasing some sides will never achieve ratio
          #so make sure to account for that infinite calculation!
        #should we check for dark edges as a clue to expand -- porbably not here
        #longside / shortside = aspectRatio
        #longside / aspectRatio = shortSide
        #longside = shortSide * aspectRatio
        ratioHighValue = max(aspect["ratio"])
        ratioLowValue = min(aspect["ratio"])
        longSideLength = boxStats["longSideLength"]
        shortSideLength = boxStats["shortSideLength"]
        newShortSideLength = ratioLowValue * longSideLength // ratioHighValue
        newLongSideLength = ratioHighValue * shortSideLength // ratioLowValue
        shortSideDelta = newShortSideLength - shortSideLength
        longSideDelta = newLongSideLength - longSideLength
        if min(shortSideDelta,longSideDelta) == shortSideDelta:
          transformAxis = boxStats["shortSideAxis"]
          transformDelta = shortSideDelta
        else:
          transformAxis = boxStats["longSideAxis"]
          transformDelta = longSideDelta

        return {"axis": transformAxis, "transformDelta": transformDelta} #transform axis, delta

      def expandToAspect(xCoord, yCoord, width, height, boxStats, aspect, allBoxes)
      #grow the box along the axis of the shorter side
      #choose direction to grow along axis
       #DO NOT grow in direction that will intersect with another box
        #if intersects, check if combo of boxes will create box close to aspect
         #if so, add combo box; if not, try other direction
       #Grow in direction with highest proportion of binary(true) pixels
      axis = boxStats["shortSideAxis"]
      newShortSideLength = longSideLength * min(aspect["ratio"]) // max(aspect["ratio"])
      delta = newShortSideLength - shortSideLength
      if axis == "x":
        #box transformed to left (A) or right (B)
        optionA = (xCoord - delta, yCoord, delta + width, height)
        optionB = (xCoord, yCoord, width + delta, height)
      else:
        #box transformed top (A) or bottom (B)
        optionA = (xCoord, yCoord - delta, width, delta + height)
        optionB = (xCoord, yCoord, width, height + delta)
        
      #check if intersects other bounding boxes (see imsearch algorithm)
      #check intersects earlier in algorithm to create combined boxes if matches aspect
      results = map()
      
      def chooseTransformDirection(box, transformAxisDetails)
        #check if transforming along axis intersects another box
        #if one side intersects a box
    def transformBox(box, transformAxisAndDirectionDetails):
      transformedBox = ()
      if(transformDetails["axis"] = x):
        doSomething
      else:
        doSomthing
      return transformedBox
    
  return list(boxes)

# only select boxes close to user defined image sizes
def onlySpecificImageSizes(boundingboxes):
  for box in boundingboxes:
  return

# send initial value 'contours' through a pipeline of functions
finalboxes = pipe(contours, limitSizes, mapContoursToBoxes, removeSubboxes)

# draw the bounding rectangle on a viewable image
for box in finalboxes:
  # draw axis-aligned bounding box

  #x,y,w,h = cv2.boundingRect(box)
  #cv2.rectangle(image, (x,y), (x+w, y+h), outlineColor, outlineWidth)
  #x: [0], y: [1], w: [2], h: [3]
  cv2.rectangle(imageforviewing, (box[0],box[1]), (box[0]+box[2],box[1]+box[3]), (255,255,0), 5)
  
  # straighten photo (will use in future)
  # draw contour-aligned bounding box
  #contourbox = cv2.minAreaRect(box)
  #corners = numpy.int0(cv2.boxPoints(contourbox)) #int0->intp
  #cv2.drawContours(im, [corners], 0, (0,0,255), 3)
  #print("angle: ", contourbox[2])


# ALL THE THINGS THAT WILL DISPLAY

# stats to display for analysis
print("Resulting Number of Images: ", len(finalboxes)) #total number of blobs after size filter

# create display window
# resize the output windows bc on WindowsOS...well, its WindosOS
# show the image

#cv2.namedWindow("Im", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("Im", 600,600)
#cv2.imshow("Im", im)

#cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("Image", 600,600)
#cv2.imshow("Image", imageforanalysis)

cv2.namedWindow("Thresh", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Thresh", 600,600)
cv2.imshow("Thresh", imageforviewing)

cv2.waitKey(0)