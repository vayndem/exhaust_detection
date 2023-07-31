import os
import cv2
import numpy as np
from PIL import Image
import mysql.connector 
import json 
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

os.environ['FLASK_ENV'] = 'development'

# Fungsi untuk mengizinkan ekstensi foto yang diizinkan
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def loadmodel(x="D:\\code\\data.onnx"):
    net = cv2.dnn.readNetFromONNX(x)
    return net

# create connection object 
con = mysql.connector.connect( 
    host="localhost", user="root", 
    password="", database="knalpota"
)
 
# create cursor object 
cursor = con.cursor() 

net = loadmodel()

classes = ["tidak standar", "standar", "motor"]

# Fungsi untuk menjalankan deteksi pada gambar
def run(img):
    filename = img.filename
    img = Image.open(img.stream)
    img = img.convert("RGB")
    img = np.array(img)
    blob = cv2.dnn.blobFromImage(img, scalefactor=1/255, size=(640, 640), mean=[0, 0, 0], swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()[0]

    counter = [0, 0, 0]
    current_counter = [0] * len(classes)

    classes_ids = []
    confidences = []
    boxes = []
    rows = detections.shape[0]

    img_width, img_height = img.shape[1], img.shape[0]
    x_scale = img_width/640
    y_scale = img_height/640

    for i in range(detections.shape[0]):
        row = detections[i]
        confidence = row[4]
        if confidence > 0.2:
            classes_score = row[5:]
            ind = np.argmax(classes_score)
            if classes_score[ind] > 0.25:
                classes_ids.append(ind)
                confidences.append(confidence)
                cx, cy, w, h = row[:4]
                x1 = int((cx - w / 2) * x_scale)
                y1 = int((cy - h / 2) * y_scale)
                width = int(w * x_scale)
                height = int(h * y_scale)
                box = np.array([x1, y1, width, height])
                boxes.append(box)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.1)

    for i in indices:
        x1, y1, w, h = boxes[i]
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

    hasil = json.dumps({
        "image": {
            "file_name": filename,
        },
        "standart": counter[1],
        "non-standart": counter[0],
        "total": counter[:2]
    })

    standar=counter[1]
    non_standar=counter[0]

    insert1 = "INSERT INTO data_knalpot (json_data, standar, non_standar) VALUES (%s, %s ,%s)"
    nilai = (hasil,standar,non_standar)
    cursor.execute(insert1, nilai)
    con.commit()

    print("Detection Result:")
    print(hasil)

    return hasil

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join('static', filename))
        result = run(file)  # Menjalankan fungsi run untuk mendeteksi dan menghitung counter
        return redirect(url_for('uploaded_file', filename=filename, result=result))
    else:
        return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    result = request.args.get("result", default="", type=str)

    standar = 0
    non_standar = 0

    print("Result from request.args:")
    print(result)

    if result:
        hasil_deteksi = json.loads(result)
        standar = hasil_deteksi.get('standart', 0)
        non_standar = hasil_deteksi.get('non-standart', 0)

        print("Standar:")
        print(standar)
        print("Non Standar:")
        print(non_standar)

    return render_template('uploaded_file.html', filename=filename, result=result, standar=standar, non_standar=non_standar)

if __name__ == '__main__':
    app.run(port=5001)
    app.run()