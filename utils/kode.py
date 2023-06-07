import cv2
import numpy as np
from PIL import Image



def loadmodel(x="D:\\code\\data.onnx"):
    net = cv2.dnn.readNetFromONNX(x)
    return net


# cap = cv2.VideoCapture("video.mp4")
# # cap = cv2.VideoCapture('pidio3.mp4')


# Tambahkan variabel counter untuk masing-masing class
counter = [0, 0, 0]



net=loadmodel()

classes = ["tidak standar", "standar", "motor"]



def run(img):

    filename = img.filename
    img=Image.open(img.stream)
    
    img=img.convert("RGB")
    img=np.array(img)
    blob = cv2.dnn.blobFromImage(img,scalefactor= 1/255,size=(640,640),mean=[0,0,0],swapRB= True, crop= False)
    net.setInput(blob)
    detections = net.forward()[0]
    
    current_counter = [0] * len(classes)

    classes_ids = []
    confidences = []
    boxes = []
    rows = detections.shape[0]

    img_width, img_height = img.shape[1], img.shape[0]
    x_scale = img_width/640
    y_scale = img_height/640

    for i in range(rows):
        row = detections[i]
        confidence = row[4]           
        if confidence > 0.2:
            classes_score = row[5:]
            ind = np.argmax(classes_score)
            if classes_score[ind] > 0.25:
                    
                    classes_ids.append(ind)
                    confidences.append(confidence)
                    cx, cy, w, h = row[:4]
                    x1 = int((cx- w/2)*x_scale)
                    y1 = int((cy-h/2)*y_scale)
                    width = int(w * x_scale)
                    height = int(h * y_scale)
                    box = np.array([x1,y1,width,height])
                    boxes.append(box)
    
    indices = cv2.dnn.NMSBoxes(boxes,confidences,0.1,0.1)

    for i in indices:
            
            x1,y1,w,h = boxes[i]
            class_id = classes_ids[i]
            label = classes[class_id]
            conf = confidences[i]
            text = label + " ({:.2f})".format(conf)


            current_counter[class_id] += 1

            if label == "motor" and classes_ids.count(1) == 0:
                counter[1] += 1
        
    for i, count in enumerate(counter):
            
            if classes_ids == 0:
                counter[i] += current_counter[i]
                if classes_ids == 0:
                    counter[1] += 2
            else:
                counter[i] = max(0, count)

    # tambahkan kode untuk menampilkan counter pada gambar
    for class_id, count in enumerate(counter):
        label = classes[class_id]
        tex = "{}: {}".format(label, count)


    return{
       
       "image":{
            "file_name": filename,
       },
       "standart" :counter[1],
       "non-standart": counter[0],

       "total" : counter[:2],

    }

