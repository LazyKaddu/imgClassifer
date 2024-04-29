from flask import Flask,  render_template ,request 
import mysql.connector
import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt

conn = mysql.connector.connect(user='root', password='Kaddulive@0', host='127.0.0.1', database='plantData')
cursor = conn.cursor()

querry = 'select * from plants where plant_name like "%{}%";'
searchQuerry = 'select * from plants where sNo like "%{}%";'

class_names = ['Arnica', 'Avaramsenna', 'Bitterorange', 'Cayenne', 'Eurphorbia', 'GA', 'Goldenseal', 'abscess', 'acai', 'alfalfaa', 'aloe', 'amargo', 'ashok', 'ashwagandha', 'bilberry', 'bittermelon', 'borage', 'cannabis', 'chamomile', 'henna', 'thristle']
classes = ['abscess', 'acai', 'alfalfaa', 'aloe', 'amargo', 'ashok', 'ashwagandha', 'Avaramsenna', 'bilberry', 'bittermelon', 'Bitterorange', 'borage', 'cannabis', 'Cayenne', 'chamomile', 'Eurphorbia', 'GA', 'Goldenseal', 'henna', 'thristle','Arnica']
model = tf.keras.models.load_model("savedModel.ckpt")

app = Flask(__name__,template_folder='templates')


NAME = 'Kabeer'
GENES = 'Human'
PART = 'Brain'
DISEASE = 'Lonliness'
FOUND = 'Pauri'
DESC = 'The one who made this website'

def preProcess(file):
    file_contents = file.read()
    nparr = np.frombuffer(file_contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.resize(img,(512,512))
    img = np.reshape(img,(1,512,512,3))

    img_normalized = cv2.normalize(img, None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    print('image processed')
    return img_normalized

def output(img):
    global model
    data = preProcess(img)
    model_output_multi_class = model.predict(data)
    multi_class_prediction = np.argmin(model_output_multi_class)
    print(multi_class_prediction)
    return multi_class_prediction

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    if request.method == 'POST':
        PLANT = request.form['search']
        print(PLANT.capitalize())
        
        try:
            cursor.execute(querry.format(PLANT.capitalize()))
            DATA = cursor.fetchall()[0]
            print(DATA)
            return render_template('results.html', name = DATA[1], genes = DATA[2], part = DATA[3], disease = DATA[4], found = DATA[5], desc = DATA[6])
        except Exception as e:
            print(e)
            return render_template('results.html',name = NAME, genes = GENES, part = PART, disease = DISEASE, found = FOUND, desc = DESC)
    else:
        return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')
    
@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        PLANT = request.files['file']
        if PLANT:
            ind = classes[output(PLANT)]
            ind = ind.capitalize()
        try:
            cursor.execute(querry.format(ind))
            DATA = cursor.fetchall()[0]
            return render_template('results.html', name = DATA[1], genes = DATA[2], part = DATA[3], disease = DATA[4], found = DATA[5], desc = DATA[6])
        except Exception as e:
            print(e)
            return render_template('results.html',name = NAME, genes = GENES, part = PART, disease = DISEASE, found = FOUND, desc = DESC)
    else:
        return render_template('index.html')

if __name__ == "__main__" :
    app.run(debug=True)

    