import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt

print('library loaded')


def preProcess(img):
    img=cv2.imread(img)
    print(img[197][452])
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
    return multi_class_prediction

class_names = ['Arnica', 'Avaramsenna', 'Bitterorange', 'Cayenne', 'Eurphorbia', 'GA', 'Goldenseal', 'abscess', 'acai', 'alfalfaa', 'aloe', 'amargo', 'ashok', 'ashwagandha', 'bilberry', 'bittermelon', 'borage', 'cannabis', 'chamomile', 'henna', 'thristle']
classes = ['abscess', 'acai', 'alfalfaa', 'aloe', 'amargo', 'ashok', 'ashwagandha', 'Avaramsenna', 'bilberry', 'bittermelon', 'Bitterorange', 'borage', 'cannabis', 'Cayenne', 'chamomile', 'Eurphorbia', 'GA', 'Goldenseal', 'henna', 'thristle','Arnica']
model = tf.keras.models.load_model("savedModel.ckpt")
print('model loaded')





print(classes[output])
