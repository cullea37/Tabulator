def fretCrop():
	from contourTrial import NeckLength
	neckLeftX ,neckRightX, BoundingBoxCoordinates = NeckLength()
	cropX = []
	for i in range(len(BoundingBoxCoordinates)):
		bottomLeft,topLeft,bottomRight,topRight = BoundingBoxCoordinates[i]
		leftX =  bottomLeft[0]
		if leftX < 0:
			leftX = 0
		cropX.append(leftX)
	return neckLeftX, neckRightX, cropX





