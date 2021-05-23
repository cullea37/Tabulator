import requests
import base64
import time, os, json
from mp4mp3 import mp4mp3
from auth import auth
from __main__ import app

def doremirscr(video):
	path = app.root_path
	mp4mp3(video)

	auth()
	f = open(path + "/scripts/auth.text", "r")
	f.seek(0)
	authresult = f.read()
	f.close()

	starturl = "https://api.doremir.com/v1/audio-to-musicxml/start"
	startheader = {'Authorization': authresult, 'Content-Type': 'application/json'}
	startpayload = {"analysisType": "monophonic", "audioFormat": "mp3"}

	resstart = requests.post(starturl, headers = startheader, json = startpayload)

	startresult = resstart.json()
	print (startresult)
	print ("startresult\n\n") 

	recordingId = startresult['recordingId']
	print (recordingId)
	print ("recordingId\n\n")

	uploadurl = "https://api.doremir.com/v1/audio-to-musicxml/upload"
	uploadheader = {'Authorization': authresult, 'Content-Type': 'application/json'}

	f = open(path+"/scripts/audio.mp3", "rb+")
	raw = f.read()
	f.close()

	encode = base64.urlsafe_b64encode(raw).decode('utf-8')

	uploadpayload = {"recordingId": recordingId, 'audio': encode}

	resupload = requests.post(uploadurl, headers = uploadheader, json = uploadpayload)

	uploadresult = resupload.json()
	print (uploadresult)
	print ("uploadresult\n\n")

	resulturl = "https://api.doremir.com/v1/audio-to-musicxml/result"
	resultheader = {'Authorization': authresult, 'Content-Type': 'application/json'}
	resultpayload = {"recordingId": recordingId}

	time.sleep(20)
	resresult = requests.post(resulturl, headers = resultheader, json = resultpayload)

	resultresult = resresult.json()
	resultresult = resultresult["musicxml"]
	try: 
		resultresult = base64.b64decode(resultresult)
	except TypeError:
		return True 

	f = open(path + "/scripts/result.xml", "wb")
	f.write(resultresult)