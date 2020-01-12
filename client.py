import socket
import os
import time
from espeakng import ESpeakNG
def speak1(text,text1):
        os.popen( 'espeak "'+text+' is at the '+text1+'" -ven-us+f4 -s120 --stdout | aplay 2>/dev/null' )
        time.sleep(2)
a=['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.43.81"
port = 8000
print (host)
##print (port)
serversocket.bind((host, port))
serversocket.listen(5)
print ('server started and listening')
while 1:
    (clientsocket, address) = serversocket.accept()
    print ("connection found!")
    data = clientsocket.recv(1024).decode()
    print (data)
    data=data.split()
    i=int(data[0])
    speak1(a[i],data[1])
    r='got it'
    clientsocket.send(r.encode())