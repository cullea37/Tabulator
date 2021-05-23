from moviepy.editor import *
from __main__ import app
import io

def mp4mp3(video):
	path = app.root_path
	video.seek(0)
	video.save(path+ "/scripts/video.mp4")
	video.seek(0)
	video.save(path+ "/static/video.mp4")
	mp4file = path+"/scripts/video.mp4"
	mp3file = path+"/scripts/audio.mp3"

	videoClip = VideoFileClip(mp4file) 
	audioClip = videoClip.audio
	audioClip.write_audiofile(mp3file)
	audioClip.close()
	videoClip.close()