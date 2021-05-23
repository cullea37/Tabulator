import cv2
import numpy as np
import glob, os, time
import re
from __main__ import app

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def NeckLengthCal():
    outputBox = []
    # Load object detector model
    path = app.root_path
    net = cv2.dnn.readNet(path+"/scripts/models/newyolov4-obj.cfg", path+"/scripts/models/newyolov4-obj_last.weights")

    # Name of class
    classes = ["GuitarNeck"]

    # Path to frame outputted by audio component
    images_path = sorted(glob.glob(path+ r"/scripts/test/*.jpg"), key=numericalSort)
    #### Info on image length feed to Fret object detector ####
    print("\nYolo images path length: \n")
    print(len(images_path))
    
    if len(images_path) == 0:
        print("Image directory is empty, please try again!")
        return [], []
    else:   

        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


        for img_path in images_path:
            # Loading image
            while not os.path.exists(img_path):
                print("INFO: waiting for write of frame YOLO" + img_path)
                time.sleep(1)
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            height, width = img.shape

            # Where the object detection takes place
            blob = cv2.dnn.blobFromImage(img, 0.00392, (608, 608), (0, 0, 0), True, crop=False)

            net.setInput(blob)
            outs = net.forward(output_layers)
   

            # produces confidence levels, and locates bounding boxes
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:

                for detection in out:

                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        centreX = int(detection[0] * width)
                        centreY = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(centreX - w / 2)
                        y = int(centreY - h / 2)

                     
                        boxes.append([ x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

            #data outputted to image, was used for presentation and debugging
            if len(boxes) != 0:
                boxesPrior = boxes
                indexesPrior = indexes
                for i in range(len(boxes)):
                    if i in indexes:
                        x, y, w, h = boxes[i]
                        q = [(x, y),(x, y + h), (x + w, y), (x + w, y + h)]

                        outputBox.append(q)
                        cv2.rectangle(img, (x, y), (x + w, y + h), 255, 2)

            if (len(boxes) == 0 and len(boxesPrior) != 0):
                for i in range(len(boxesPrior)):
                    if i in indexesPrior:   
                        x, y, w, h = boxesPrior[i]
                        q = [(x, y),(x, y + h), (x + w, y), (x + w, y + h)]
                        
                        outputBox.append(q)
                        cv2.rectangle(img, (x, y), (x + w, y + h), 255, 2)

            #### uncomment for images of fretboard detection #####        
            #img = cv2.resize(img, None, fx=0.5, fy=0.5)
            #cv2.imshow("Image", img)
            #key = cv2.waitKey(0)

    cv2.destroyAllWindows()
    if len(outputBox) != len(images_path):
        print("Not all extracted frames contain boundingBoxs please input clear images")
        return [], []
    else: 
        return outputBox ,images_path   
