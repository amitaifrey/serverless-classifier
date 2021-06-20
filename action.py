#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
from tensorflow.keras.applications import NASNetMobile
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.nasnet import preprocess_input, decode_predictions
import numpy as np
import base64

def main(dict):
    print(os.listdir("/root/.keras/models")) 
    try:
        model = NASNetMobile()
        img = tf.io.decode_base64(dict['image'])
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, [224,224])
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x.copy()
        x = preprocess_input(x)
        preds = model.predict(x)
        top5 = decode_predictions(preds, top=5)[0]
        result = []
        for pred in top5:
            result.append({pred[1]: str(pred[2])})
        return { 
            'result': result 
        }
    except Exception as e:
        return {'error' : str(e)}
