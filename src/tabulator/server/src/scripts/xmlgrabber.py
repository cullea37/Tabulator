import xml.etree.ElementTree as ET
from doremirscr import doremirscr
import os
import time
import cv2
from __main__ import app
from super_res_image import superRes

def xmlgrabber(video):
	returnError = doremirscr(video)
	if returnError == True:
		return []

	path = app.root_path
	#### empty frame folder from last run ####
	
	tree = ET.parse(path + '/scripts/result.xml')
	root = tree.getroot()
	noteslist = []
	notedict = {}
	tempo = root.find("part").find("measure").find("direction").find("sound").get("tempo")
	beats = int(root.find("part").find("measure").find("attributes").find("time").find("beats").text)
	beats = 4/beats
	timestamps = []
	bps = beats*(60/float(tempo)) 

	current_time = 0.0 

	for part in root.findall("part"):
		for measure in part.findall("measure"):
			for note in measure.findall("note"):
				duration, dynamics = str(float(note.find("duration").text)/1024), note.get("dynamics")
				try:
					pitch = note.find("pitch").find("step").text
					if note.find("pitch").find("alter") != None:
						pitch = pitch + "#"
					pitch = pitch + note.find("pitch").find("octave").text
					if note.find("tie") != None:
						if note.find("tie").get("type") == "stop":
							length = len(noteslist)
							oldnotesduration = noteslist[length -1].get("duration")
							noteslist[length -1]["duration"] = str(float(oldnotesduration)+ float(duration))
							current_time = current_time + float(notedict.get("duration")) * bps
						else:
							notedict = {"note" : pitch, "duration" : duration, "dynamics" : dynamics}
							noteslist.append(notedict)
							timestamps.append(str(current_time))

					else:
						notedict = {"note" : pitch, "duration" : duration, "dynamics" : dynamics}
						length = len(noteslist)
						######### Eliminate ghost notes when the same note is heard again but less loud ################
						if length == 0:
							noteslist.append(notedict)
							timestamps.append(str(current_time))
							current_time = current_time + float(notedict.get("duration")) * bps
						elif (notedict["note"] == noteslist[length -1].get("note") and (int(notedict["dynamics"])/ int(noteslist[length -1].get("dynamics"))) < .9):
							oldnotesduration = noteslist[length -1].get("duration")
							noteslist[length -1]["duration"] = str(float(oldnotesduration)+ float(duration))
							current_time = current_time + float(notedict.get("duration")) * bps
						else:
							noteslist.append(notedict)
							timestamps.append(str(current_time))
							current_time = current_time + float(notedict.get("duration")) * bps
				except AttributeError:
					notedict = {"duration" : duration}
					noteslist.append(notedict)
					timestamps.append(str(current_time))
					current_time = current_time + float(notedict.get("duration")) * bps
	#### remove leading rests from noteslist ####
	i = 0
	print("INFO: Timestamps; xmlgrabber")
	print(len(timestamps))
	print(timestamps)
	oldtimestamps = timestamps
	timestamps = []
	restduration = 0
	for elem in noteslist:
		if "note" in elem:
			break
		else:
			restduration += float(elem["duration"]) * bps
			i += 1
	while i > 0:
		noteslist.pop(0)
		oldtimestamps.pop(0)
		i -= 1
	for elem in oldtimestamps:
		timestamps.append(str(float(elem) - restduration))


	vidcap = cv2.VideoCapture(path+'/scripts/video.mp4')
	fps = vidcap.get(cv2.CAP_PROP_FPS)
	frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
	success,image = vidcap.read()
	count = 0
	success = True
	i = 0
	print(timestamps)
	try:
		while success:
			success,frame = vidcap.read()
			if abs(count/fps - float(timestamps[i])) <= abs((count+1)/fps - float(timestamps[i])):
				frame = superRes(frame)
				cv2.imwrite(path +'/scripts/test/frame%d.jpg'%i,frame)
				i=i+1

			count+=1

	except:
		pass
	##### Add frames for notes at the end where timestamps go past endpoint from calculation error #####
	while i < len(timestamps):
		vidcap.set(cv2.CAP_PROP_POS_FRAMES, count-1)
		success, frame = vidcap.read()
		frame = superRes(frame)
		cv2.imwrite(path +'/scripts/test/frame%d.jpg'%i,frame)
		i += 1
		print("Warning: capture taken at last frame")
	i-=1
	while not os.path.exists(path +'/scripts/test/frame%d.jpg'%i):
		print("INFO: waiting for write of frames")
		time.sleep(1)
	return noteslist