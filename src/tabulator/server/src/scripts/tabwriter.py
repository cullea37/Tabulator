
def tabwriter(noteslist):
	f = open("tab.txt", "w+")
	newLineCounter = 0
	breakFlag = False
	while noteslist != []:
		i = 0
		noteCounter = 0
		while i != 6: #### iterate through list for each string ####
			newLineCounter = 0
			if i == 0:
				f.write("e|-")
				barCounter = 0
				for elem in noteslist:

					if barCounter >= 24: ##### write | for every bar #####
						barCounter = 0
						newLineCounter += 1
						if newLineCounter == 3:
							if noteCounter > len(noteslist):
								breakFlag = True
							break
						f.write("|-")

					elemDuration = int(float(elem["duration"]) * 6)
					barCounter += elemDuration
					try:
						if elem["position"][0] == 1: #### check that note is played on current string ####
							f.write(str(elem["position"][1]))
							if elem["position"][1] < 10:
								f.write("-"*(elemDuration - 1))
							else: 
								f.write("-"*(elemDuration - 2))
						else:
							f.write("-"*(elemDuration))
					except KeyError: 
						f.write("-"*(elemDuration))
					noteCounter += 1
				f.write("|")

			elif i == 1:
				f.write("B|-")
				barCounter = 0
				for elem in noteslist:

					if barCounter >= 24: ##### write | for every bar #####
						barCounter = 0
						newLineCounter += 1
						if newLineCounter == 3:
							break
						f.write("|-")

					elemDuration = int(float(elem["duration"]) * 6)
					barCounter += elemDuration
					try:
						if elem["position"][0] == 2: #### check that note is played on current string ####
							f.write(str(elem["position"][1]))
							if elem["position"][1] < 10:
								f.write("-"*(elemDuration - 1))
							else: 
								f.write("-"*(elemDuration - 2))
						else:
							f.write("-"*(elemDuration))
					except KeyError:
						f.write("-"*(elemDuration))
				f.write("|")
			elif i == 2:
				f.write("G|-")
				barCounter = 0
				for elem in noteslist:

					if barCounter >= 24: ##### write | for every bar #####
						barCounter = 0
						newLineCounter += 1
						if newLineCounter == 3:
							break
						f.write("|-")

					elemDuration = int(float(elem["duration"]) * 6)
					barCounter += elemDuration
					try:
						if elem["position"][0] == 3: #### check that note is played on current string ####
							f.write(str(elem["position"][1]))
							if elem["position"][1] < 10:
								f.write("-"*(elemDuration - 1))
							else: 
								f.write("-"*(elemDuration - 2))
						else:
							f.write("-"*(elemDuration))
					except KeyError:
						f.write("-"*(elemDuration))
				f.write("|")
			elif i == 3:
				f.write("D|-")
				barCounter = 0
				for elem in noteslist:

					if barCounter >= 24: ##### write | for every bar #####
						barCounter = 0
						newLineCounter += 1
						if newLineCounter == 3:
							break
						f.write("|-")

					elemDuration = int(float(elem["duration"]) * 6)
					barCounter += elemDuration
					try:
						if elem["position"][0] == 4: #### check that note is played on current string ####
							f.write(str(elem["position"][1]))
							if elem["position"][1] < 10:
								f.write("-"*(elemDuration - 1))
							else: 
								f.write("-"*(elemDuration - 2))
						else:
							f.write("-"*(elemDuration))
					except KeyError:
						f.write("-"*(elemDuration))
				f.write("|")
			elif i == 4:
				f.write("A|-")
				barCounter = 0
				for elem in noteslist:

					if barCounter >= 24: ##### write | for every bar #####
						barCounter = 0
						newLineCounter += 1
						if newLineCounter == 3:
							break
						f.write("|-")

					elemDuration = int(float(elem["duration"]) * 6)
					barCounter += elemDuration
					try:
						if elem["position"][0] == 5: #### check that note is played on current string ####
							f.write(str(elem["position"][1]))
							if elem["position"][1] < 10:
								f.write("-"*(elemDuration - 1))
							else: 
								f.write("-"*(elemDuration - 2))
						else:
							f.write("-"*(elemDuration))
					except KeyError:
						f.write("-"*(elemDuration))
				f.write("|")
			elif i == 5:
				f.write("E|-")
				barCounter = 0
				for elem in noteslist:

					if barCounter >= 24: ##### write | for every bar #####
						barCounter = 0
						newLineCounter += 1
						if newLineCounter == 3:
							f.write("|")
							f.write("\n\n")
							break
						f.write("|-")

					elemDuration = int(float(elem["duration"]) * 6)
					barCounter += elemDuration
					try:
						if elem["position"][0] == 6: #### check that note is played on current string ####
							f.write(str(elem["position"][1]))
							if elem["position"][1] < 10:
								f.write("-"*(elemDuration - 1))
							else: 
								f.write("-"*(elemDuration - 2))
						else:
							f.write("-"*(elemDuration))
					except KeyError:
						f.write("-"*(elemDuration))
				oldnoteslist = noteslist
				noteslist = oldnoteslist[noteCounter:]
				if noteslist == []:
					f.write("|")



			f.write("\n")
			i += 1
		if breakFlag == True:
			break

	f.close()
