def removeOutDistance(XList,YList,averageCountX,averageCountY,xCount,yCount):
	count = 0
	x2 = averageCountX
	y2 = averageCountY
	errorListX = XList
	errorListY = YList
	for i in range(len(XList)):
		x1 = XList[i][0]
		y1 = YList[i][0]
		# make this number a scale factor of the length of the neck of the guitar, or a set percentage outside of mean value
		if (math.sqrt((x2-x1)**2 + (y2-y1)**2)) > 150:
			errorListY.pop(i)
			errorListX.pop(i)
			xCount = xCount-x1
			yCount = yCount-y1
			averageCountX =	(xCount)/(len(XList) - count)
			averageCountY =	(xCount)/(len(YList) - count)
	averageCord = (averageCountX,averageCountY)					
	count = 0		
	for i in range(len(errorListY)):
		x1 = XList[i][0]
		y1 = YList[i][0]
		if errorListY[i][0] > averageCountY:
			count += 1
			xCount = xCount-x1			
			yCount = yCount-y1
	averageCountX =	(xCount)/(len(XList) - count)
	averageCountY =	(yCount)/(len(YList) - count)
	averageCord = (averageCountX,averageCountY)	
	return averageCord	

def HandLocation(cropX):
	from HandPose import estimatePoints
	allImagesPointList = estimatePoints(cropX)
	OutputListOfHandPoints = []
	averageCountXList = []
	averageCountYList = []
	errorString = ""

	KeyPoints = [6,7,8,10,11,12,14,15,16,18,19,20]
	n = 0 
	for points in allImagesPointList:
		x = 0
		y = 0
		x3 = 0
		y3 = 0
		XList = []
		YList = []
		XList1 = []
		YList1 = []
		for i in range(len(points)):

			if points[i] == None or i not in KeyPoints:
				pass
			else:
				x = points[i][0]
				x1 = (x,i)
				XList.append(x1)
				y = points[i][1]
				y1 = (y,i)
				YList.append(y1)

			if points[i] == None:
				pass
			else:		
				x3 = points[i][0]
				x2 = (x3,i)
				y3 = points[i][1]
				y2 = (y3,i)
				XList1.append(x2)
				YList1.append(y2)	
		xCount = 0
		yCount = 0
		if len(XList1) > 0:
			for j in range(len(XList1)):
				xCount = XList1[j][0] + xCount
				yCount = YList1[j][0] + yCount			
			averageCountX =	xCount/len(XList1)
			averageCountY =	yCount/len(YList1)


			print("Handpoints list before")
			print(OutputListOfHandPoints)

			averageCord = removeOutDistance(XList1,YList1,averageCountX,averageCountY,xCount,yCount)
			OutputListOfHandPoints.append(averageCord)
			print("Handpoints list after")
			print(OutputListOfHandPoints)
	
			
		elif len(XList) > 0 and  len(XList1) == 0:
			for j in range(len(XList)):
				
				xCount = XList[j][0] + xCount
				yCount = YList[j][0] + yCount					
			averageCountX =	xCount/len(XList)
			averageCountY =	yCount/len(YList)
			averageCord = removeOutDistance(XList1,YList1,averageCountX,averageCountY,xCount,yCount)

			OutputListOfHandPoints.append(averageCord)
			print("Removing outliers")
			print(OutputListOfHandPoints)

		else:
			print(OutputListOfHandPoints)
			print(n)
			try:
				OutputListOfHandPoints.append(OutputListOfHandPoints[len(OutputListOfHandPoints)-1])
			except IndexError:
				OutputListOfHandPoints.append(None)
			errorString += "Hand not found for note: " + str(n) + "\n"
		print(OutputListOfHandPoints)
		#print(n)
		n += 1

	return OutputListOfHandPoints, errorString
		 



