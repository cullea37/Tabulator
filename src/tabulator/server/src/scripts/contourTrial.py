import cv2 as cv
import numpy as np


# Preprocessing is applied to the cropped image here, the finished result is a binary image
def preprocessing(img):
	img = cv.GaussianBlur(img,(9,9), 1)
	img = cv.GaussianBlur(img,(9,9), 1)
	img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
								cv.THRESH_BINARY, 15, -2)
	return img

#Here the horizontal structures in the img are extracted
def horizontalStructure(horizontal,thresh):
	cols = horizontal.shape[1]
	horizontal_size = cols // thresh
	horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
	horizontal = cv.erode(horizontal, horizontalStructure)
	horizontal = cv.erode(horizontal, horizontalStructure)
	horizontal = cv.dilate(horizontal, horizontalStructure)
	#cv.imshow("horizontal", horizontal) #used for testing
	#cv.waitKey(0)
	return horizontal


def verticalStructure(vertical,thresh):
	rows = vertical.shape[0]
	verticalsize = rows // thresh
	verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, verticalsize))
	vertical = cv.erode(vertical, verticalStructure)
	vertical = cv.erode(vertical, verticalStructure)
	vertical = cv.dilate(vertical, verticalStructure)
	#cv.imshow("vertical", vertical) #used for testing
	#cv.waitKey(0)
	return vertical
	
def VerticalLines(vertical):
	edges = cv.adaptiveThreshold(vertical, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
	                                cv.THRESH_BINARY, 3, -2)
	kernel = np.ones((2, 2), np.uint8)
	edges = cv.dilate(edges, kernel)
	blurred = np.copy(vertical)
	blurred = cv.blur(blurred, (2, 2))
	(rows, cols) = np.where(edges != 1)
	vertical[rows, cols] = blurred[rows, cols]
	return vertical

def HorizontalLines(horizontal):
	edges = cv.adaptiveThreshold(horizontal, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
	                                cv.THRESH_BINARY, 3, -2)
	kernel = np.ones((2, 2), np.uint8)
	edges = cv.dilate(edges, kernel)
	blurred = np.copy(horizontal)
	blurred = cv.blur(blurred, (2, 2))
	(rows, cols) = np.where(edges != 0)
	horizontal[rows, cols] = blurred[rows, cols]
	return horizontal	

def VerticalHough(verticalLines):
	blank = np.zeros(verticalLines.shape[:2], dtype='uint8')
	lines = cv.HoughLinesP(verticalLines, 1, np.pi,20,minLineLength=40,maxLineGap=5)
	x = type(lines)
	if x == type(None):
		#print("can't draw vertical hough lines, no lines detected that fit the parameters")
		return False , blank
	else:	
		for line in lines:
			x1,y1,x2,y2 = line[0]
			cv.line(blank,(x1,y1), (x2,y2), (255,255,255),1)
	return True, blank	

def HorizontalHough(HLines):
	blank = np.zeros(HLines.shape[:2], dtype='uint8')
	lines = cv.HoughLinesP(HLines, 1, np.pi/180,100,minLineLength=int(HLines.shape[1]/1.2),maxLineGap=100)
	x = type(lines)
	if x == type(None):
		#print("can't draw horizontal hough lines, threshhold increased")
		return False , blank

	else:	
		for line in lines:
			x1,y1,x2,y2 = line[0]
			cv.line(blank,(x1,y1), (x2,y2), (255,255,255),5)	
	return True, blank	


def RemoveShortVerticalContours(HoughVertical):
	FilteredContours = np.zeros(HoughVertical.shape[:2], dtype='uint8')
	canny = cv.Canny(HoughVertical,255,255)
	contours,hierarchy = cv.findContours(canny,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

	for cnt in contours:
		cv.drawContours(FilteredContours,cnt,-1,(255,0,255),1)

	return FilteredContours	


def RemoveShortHorizontalContours(HoughHorizontal):
	FilteredContours = np.zeros(HoughHorizontal.shape[:2], dtype='uint8')
	canny = cv.Canny(HoughHorizontal,255,255)
	contours,hierarchy = cv.findContours(canny,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

	for cnt in contours:
		cv.drawContours(FilteredContours,cnt,-1,(255,255,255),1)

	return FilteredContours	


def finalContours(RemoveShortHorizontalContours):
	#blank = np.zeros(RemoveShortHorizontalContours.shape[:2], dtype='uint8') # her for testing purposes
	canny = cv.Canny(RemoveShortHorizontalContours,255,255)
	contours,hierarchy = cv.findContours(RemoveShortHorizontalContours,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
	#cv.drawContours(blank,contours,-1,(255,0,255),1)

	finalContours = []

	for cnt in contours:
		contourLength = cv.arcLength(cnt, True)
		approx = cv.approxPolyDP(cnt, 0.02 * contourLength,True)
		bbox = cv.boundingRect(approx)

		if contourLength >= (RemoveShortHorizontalContours.shape[1]/1.2):
			finalContours.append([len(approx),contourLength,approx,bbox,cnt])

	return finalContours	

def FinalCals(finalContours,img):
	blank = np.zeros(img.shape[:2], dtype='uint8')
	finalContours = sorted(finalContours,key = lambda x:x[1], reverse = True)
	for con in finalContours:
		cv.drawContours(blank,con[4],-1,(255,255,255),1)
	
	#error string here
	if len(finalContours) == 0:
		print(" No Contours found in finalContours, please provide a clearer video!")
		exit()

	else:
		line = finalContours[0][2]
		line1 = line
		#cv.line(blank,(line[0][0][0],line[0][0][1]),(line[1][0][0],line[1][0][1]), (255,255,255),1) #used for testing
		#cv.line(blank,(line[0][0][0],line[0][0][1] + 70),(line[1][0][0],line[1][0][1] + 70), (255,255,255),1)
		line1[1][0][0] = line1[1][0][0] + 70
		line1[1][0][1] = line1[1][0][1] + 70
		square = np.concatenate((line, line1))

	return square			

def CropCals(points):
	x = []
	y = []
	for i in range(4):
			x.append(points[i][0][0])
			y.append(points[i][0][1])

	xMax = max(x)
	yMin = min(y)
	yMax = max(y)		

	return xMax,yMin,yMax



def NeckLength():
	from yolo_object_detection import NeckLengthCal
	neckLeftX = []
	neckRightX = []


	pointList, images = NeckLengthCal()
	for i in range(len(images)):
		img = cv.imread(images[i])

		bottomLeft,topLeft,bottomRight,topRight = pointList[i]
		leftX =  bottomLeft[0]
		rightX = topRight[0]
		topY = bottomRight[1]
		bottomY = topRight[1]
		if leftX < 0:
			leftX = 0
		if rightX > img.shape[1]:
			rightX = img.shape[1]
		if topY < 0:
			topY = 0
		if bottomY > img.shape[0]:
			bottomY =  img.shape[0]
		else:
			pass


		img = img[topY - 50:bottomY + 50 ,leftX:rightX+50]
		blank = np.zeros(img.shape[:2], dtype='uint8')
		img = preprocessing(img)

		##apply error handling so thresh doesn't reach to high a value
		stop = False
		thresh = 5

		while stop != True:
			horizontal = horizontalStructure(img, thresh)
			horzontalLines = HorizontalLines(horizontal)
			stop , binaryHorizontalHoughLines = HorizontalHough(horzontalLines)
			thresh = thresh + 5

		stop = False
		thresh = 30

		while stop != True:
			vertical = verticalStructure(img,thresh)
			verticalLines = VerticalLines(vertical)
			stop , binaryVerticalHoughLines = VerticalHough(verticalLines)
			thresh = thresh + 5	

		RemoveVerticalContours = RemoveShortVerticalContours(binaryVerticalHoughLines)
		RemoveHorizontalContours = RemoveShortHorizontalContours(binaryHorizontalHoughLines)
		longestContours = finalContours(RemoveHorizontalContours)

		finalCal = FinalCals(longestContours,binaryHorizontalHoughLines)
		width,top,bottom = CropCals(finalCal)



		blank = binaryVerticalHoughLines[top:bottom,0:width]

		y = np.where((blank == 255))
		try: 
			minX = min(y[1])
		except ValueError:
			return [], [], []
		blank = binaryVerticalHoughLines[top:bottom,minX:width]
		#### uncomment for images of edge detection ####
		#cv.imshow("blank",blank)
		#cv.imshow("img", img)
		#cv.waitKey(0)

		length = blank.shape[1]
		LeftX = 0 + minX + leftX
		RightX = blank.shape[1] + minX + leftX
		neckLeftX.append(LeftX)
		neckRightX.append(RightX)

	return neckLeftX,neckRightX, pointList






