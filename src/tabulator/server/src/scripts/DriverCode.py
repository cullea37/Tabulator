from Fret_crop_calculations import fretCrop
from HandPositionCalculation import HandLocation
from xmlgrabber import xmlgrabber
from lookuptable import lookuptable, fretPos
from tabwriter import tabwriter
import threading
from errorhandler import errorhandler
import os, cv2
from __main__ import app

def DriverCode(video):
	#### Delete previous frames ####
	path = app.root_path
	framedirectory = path + "/scripts/test"
	for f in os.listdir(framedirectory):
		os.remove(os.path.join(framedirectory, f))

	##### Send Video to DoReMir API ####
	noteslist = xmlgrabber(video)
	if len(noteslist) == 0:
		print("\nError: Could not analyse audio\n")
		errorString = "Could not analyse audio, please play notes clearly with no background audio."
		errorhandler(errorString)
		return None
	print("\nINFO: Driver noteslist 1\n")
	print(len(noteslist))
	print(noteslist)

	##### Get FretBoard Location in images ####
	LeftX, RightX, cropX = fretCrop()
	poslist = []
	##### Get Hand Position in images ####
	HandCoordinates, errorString = HandLocation(cropX)
	if HandCoordinates[0] == None:
		if HandCoordinates[1] != None:
			HandCoordinates[0] = HandCoordinates[1]
		else:
			errorString = "Hand can not be detected, please use clear lighting and plain background in video.\n\nLet the whole guitar be present in the center of frame."
			HandCoordinates = []
	breakFlag = 0

	##### Account for crops in relative position calculation #####
	try:
		for i in range(len(RightX)):
			curval = RightX[i]-LeftX[i]
			#print("LeftX:" + str(LeftX[i]))
			#print("RightX:" + str(RightX[i]))
			#print(HandCoordinates[i][0])
			poslist.append(curval)
	except IndexError:
		print("\nError: Displaying error message without tabs\n")
		errorhandler(errorString)
		breakFlag = 1

	if breakFlag == 0:
		relativeposlist = []
		i = 0

		print("\nLength of HandCoordinates, LeftX, and poslist: \n")
		print(len(HandCoordinates))
		print(HandCoordinates)
		print(len(LeftX))
		print(len(poslist))
		print("\n")

		#### Calculate relative position of the hand to the fretboard ####

		while i < len(HandCoordinates):

			relativepos = 1 - (HandCoordinates[i][0] - LeftX[i] + poslist[i] * .39) / (poslist[i]*1.39)
			relativeposlist.append(relativepos)
			i = i+1

		print(len(relativeposlist))
		print(len(noteslist))
		
		##### Find nearest playable position for each note #####

		i = 0
		for elem in noteslist:
			if "note" in elem.keys():
				closest = lookuptable[elem["note"]][0]
				##### If you can play an open string for this note bias it when it was more likely played #####
				openOption = False
				print("\n"+ elem["note"]+ "\n")
				for position in lookuptable[elem["note"]]:
					print(position)
					if 0 in position:
						openOption = position
					if abs(fretPos(position[1]) - relativeposlist[i]) < abs(fretPos(closest[1]) - relativeposlist[i]):
						closest = position
				print(closest)
				print(abs(fretPos(closest[1]) - relativeposlist[i]))
				print(relativeposlist[i])
				print(openOption)
				if openOption != False:
					print("in openOption")
					if (abs(fretPos(closest[1]) - relativeposlist[i])) > .05:
						#### More bias when hand is closer to the nut of the guitar ####
						if relativeposlist[i] < .2:
							closest = openOption
						elif (abs(fretPos(closest[1]) - relativeposlist[i])) > .08:
							closest = openOption
				elem["position"] = closest
				print(closest)
				i+=1

		print(noteslist)
		#### Write Guitar Tabs #####
		tabwriter(noteslist)
	else:
		pass