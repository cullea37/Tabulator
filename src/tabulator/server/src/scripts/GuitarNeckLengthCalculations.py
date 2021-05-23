
import math
def NeckLength():
	from yolo_object_detection import NeckLengthCal

	pointList, immages = NeckLengthCal()
	boundingBoxLengths = []
	boundingBoxCoordinates = []

	for i in range(len(pointList)):
		bottomLeft,topLeft,bottomRight,TopRight = pointList[i]
		boundingBoxCoordinates.append(pointList[i])
		x1,y1 = bottomLeft
		x2,y2 = bottomRight
		x = math.hypot(x2 - x1, y2 - y1)
		boundingBoxLengths.append(x)

	return boundingBoxLengths, boundingBoxCoordinates 



	



