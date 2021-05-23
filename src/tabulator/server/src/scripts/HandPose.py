from __future__ import division
import cv2
import time, re
import numpy as np
import glob, os, math
from __main__ import app

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def estimatePoints(cropX):
    path = app.root_path
    protoFile = path + "/scripts/models/pose_deploy.prototxt"
    weightsFile = path+ "/scripts/models/pose_iter_102000.caffemodel"
    nPoints = 22
    allImagesPointList = []
    POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]
    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
    images_path = sorted(glob.glob(path+ r"/scripts/test/*.jpg"), key=numericalSort)
    #### Info on images fed to handpose detection ####
    print("\nHandPose images path length \n")
    print(len(images_path))
    if len(images_path) == 0:
        print("Image directory is empty, please try again!")
        return []
    else:
        j = 0
        print(cropX)
        print(len(cropX))
         # Will read in files from image path
        for frame in images_path:
            while not os.path.exists(frame):
                print("INFO: waiting for write of frame HandPose" + frame)
                time.sleep(1)
            frame = cv2.imread(frame)
            height ,width ,_ = frame.shape
            cropX[j] = cropX[j] - (cropX[j] * 0.05)
            images_path[j] = frame[0:height,int(cropX[j]):width]
            j = j + 1
        j = 0
        for frame in images_path:
            frameCopy = np.copy(frame)
            frameWidth = frame.shape[1]
            frameHeight = frame.shape[0]
            aspect_ratio = frameWidth/frameHeight

            threshold = 0.35

            t = time.time()
            # input image dimensions for the network
            inHeight = 512
            inWidth = int(((aspect_ratio*inHeight)*8)//8)
            inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)

            net.setInput(inpBlob)

            output = net.forward()

            # Empty list to store the detected keypoints
            points = []
            cropPoints = []

            for i in range(nPoints):
                # Extracts points from the probability map, if the probability is greater then the threshold appends to list
                probMap = output[0, i, :, :]
                probMap = cv2.resize(probMap, (frameWidth, frameHeight))

                minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

                if prob > threshold :
                    cv2.circle(frameCopy, (int(point[0]), int(point[1])), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED) # used to display results on the screen
                    cv2.putText(frameCopy, "{}".format(i), (int(point[0]), int(point[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA) # used to display results on the screen

                    # Add the point to the list if the probability is greater than the threshold
                    cropPoints.append((int(point[0]) + int(cropX[j]), int(point[1])))
                    points.append((int(point[0]), int(point[1])))
                else :
                    cropPoints.append(None)
                    points.append(None)

            allImagesPointList.append(cropPoints)       

            for pair in POSE_PAIRS:
                partA = pair[0]
                partB = pair[1]

                if points[partA] and points[partB]:
                    cv2.line(frame, points[partA], points[partB], (0, 255, 255), 2) # used to display results on the screen
                    cv2.circle(frame, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED) # used to display results on the screen
                    cv2.circle(frame, points[partB], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED) # used to display results on the screen

            #### uncomment for images of hand detection ####
            #frameCopy = cv2.resize(frameCopy, None, fx=0.5, fy=0.5)
            #cv2.imshow('Output-Keypoints', frame)

            #frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
            #cv2.imshow('Output-Skeleton', frame)

            #cv2.waitKey(0)
            j = j + 1
                 
            
    if len(allImagesPointList) != 0:
        return allImagesPointList
    else:
        print("No hand detected, please try again!", flush=True)
        return []