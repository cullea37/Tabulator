
def superRes(image):
	import sys
	import time
	import cv2
	import os
	import glob
	from __main__ import app
	#images_path = sorted(glob.glob(r"test/*.jpg"))
	path = app.root_path
	model_path = path + "/scripts/models/FSRCNN_x4.pb"

	modelName = model_path.split(os.path.sep)[-1].split("_")[0].lower()

	modelScale = model_path.split("_x")[-1]
	modelScale = int(modelScale[:modelScale.find(".")])

	sr = cv2.dnn_superres.DnnSuperResImpl_create()
	sr.readModel(model_path)
	sr.setModel(modelName, modelScale)

		
	#print("[INFO] w: {}, h: {}".format(image.shape[1], image.shape[0]))
	#start = time.time()
	upscaled = sr.upsample(image)
	#upscaled = sr.upsample(upscaled)
	#end = time.time()
	#print("[INFO] super resolution took {:.6f} seconds".format(end - start))
	#print("[INFO] w: {}, h: {}".format(upscaled.shape[1],upscaled.shape[0]))

	#start = time.time()
	#bicubic = cv2.resize(image, (upscaled.shape[1], upscaled.shape[0]),interpolation=cv2.INTER_CUBIC)
	#end = time.time()
	#print("[INFO] bicubic interpolation took {:.6f} seconds".format(end - start))

	#image = cv2.resize(image, None, fx=2, fy=2)
	#cv2.imshow("Original", image)
	#cv2.imshow("image", image)
	#upscaled = cv2.resize(upscaled, None, fx=0.5, fy=0.5)
	#cv2.imshow("Super Resolution", upscaled)


	#cv2.waitKey(0)
	return upscaled