# USAGE
# python maskrcnn_predict.py --weights mask_rcnn_coco.h5 --labels coco_labels.txt --image images/30th_birthday.jpg

# import the necessary packages
from mrcnn.config import Config
from mrcnn import model as modellib
from mrcnn import visualize
#from imutils.video import VideoStream
from imutils.video import FPS
#import numpy as np
import socket
import colorsys
import argparse
import imutils
import random
import cv2
import os
import time
def send(a,pos):
    jk=a+' '+pos
    print(jk)
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host="192.168.43.81"
    port=8000
    s.connect((host,port))
    s.send(jk.encode())
    
   
            
    # construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--weights", required=True,
	help="path to Mask R-CNN model weights pre-trained on COCO")
ap.add_argument("-l", "--labels", required=True,
	help="path to class labels file")
args = vars(ap.parse_args())

# load the class label names from disk, one label per line
CLASS_NAMES = open(args["labels"]).read().strip().split("\n")
print(CLASS_NAMES)

# generate random (but visually distinct) colors for each class label
# (thanks to Matterport Mask R-CNN for the method!)
hsv = [(i / len(CLASS_NAMES), 1, 1.0) for i in range(len(CLASS_NAMES))]
COLORS = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
random.seed(42)
random.shuffle(COLORS)

class SimpleConfig(Config):
	# give the configuration a recognizable name
	NAME = "coco_inference"

	# set the number of GPUs to use along with the number of images
	# per GPU
	GPU_COUNT = 1
	IMAGES_PER_GPU = 1

	# number of classes (we would normally add +1 for the background
	# but the background class is *already* included in the class
	# names)
	NUM_CLASSES = len(CLASS_NAMES)

# initialize the inference configuration
config = SimpleConfig()

# initialize the Mask R-CNN model for inference and then load the
# weights
print("[INFO] loading Mask R-CNN model...")
model = modellib.MaskRCNN(mode="inference", config=config,
	model_dir=os.getcwd())
model.load_weights(args["weights"], by_name=True)

vs = cv2.VideoCapture('http://192.168.43.81:8081')
time.sleep(2.0)
fps = FPS().start()
# load the input image, convert it from BGR to RGB channel
# ordering, and resize the image
while True:
    count=0
    ret,image=vs.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = imutils.resize(image, width=400)
    print("[INFO] making predictions with Mask R-CNN...")
    r = model.detect([image], verbose=1)[0]
    for i in range(0, r["rois"].shape[0]):
        classID = r["class_ids"][i]
        mask = r["masks"][:, :, i]
        color = COLORS[classID][::-1]
        image = visualize.apply_mask(image, mask, color, alpha=0.5)
        if classID==1 and count!=0:
            continue
        elif classID==1 and count==0:
            count+=1
            
        avg=(int(r["rois"][i][1])+int(r["rois"][i][3]))/2
        print(avg)
        if avg<130 :
            pos='left'
        elif avg>270 :
            pos='right'
        else :
            pos='front'
       # print(pos) 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow("Frame", image)
        send(str(classID),pos)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
cv2.waitKey()