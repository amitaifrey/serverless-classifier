#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import datetime
import sys
import os
# Supress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
from tensorflow.keras.applications import NASNetMobile
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.nasnet import preprocess_input, decode_predictions
import numpy as np
import base64

def main(dict):
    # Start timing the function's runtime
    start = datetime.datetime.now()
    try:
        # Load the model
        model = NASNetMobile()

        # Convert the image from a base64 string in the JSON reuqest to a numpy matrix
        img = tf.io.decode_base64(dict['image'])
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, [224,224])
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x.copy()
        x = preprocess_input(x)

        # Classify the model and get the top 5 results
        preds = model.predict(x)
        top5 = decode_predictions(preds, top=5)[0]
        result = []
        for pred in top5:
            result.append({pred[1]: str(pred[2])})

        # Calculate the total elapsed time
        end = datetime.datetime.now()
        elapsed = end - start

        # Return the predictions and the time the classification took
        return { 
            'result': result,
            'duration': str(elapsed.seconds) + "." + str(int(elapsed.microseconds / 1000)),
        }    
    except Exception as e:
        # If an excpetion was thrown, return it to the user so they know what happened
        return {'error' : str(e)}
