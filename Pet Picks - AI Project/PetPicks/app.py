from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf


app = Flask(__name__)

# load the model
model = tf.keras.models.load_model('model.h5')

# define the target image size for the model
target_size = (224, 224)

# function to preprocess the uploaded image
def preprocess_image(image_path):
    img = Image.open(image_path) # 'Image' function from "pillow" to catch the file and convert it into an image
    img = img.resize(target_size)
    # Convert the image to an array to feed it into the model using "numpy"
    img_array = np.array(img) / 255.0 # Normalize pixel values to [0,1]
    img_array = np.expand_dims(img_array, axis=0) # Add batch dimension

    return img_array


@app.route('/')
def home():
    return render_template('index.html')


# Route to handle image uploads and classification
@app.route('/upload', methods=['POST'])
def upload():
    
    # Store the files from the contained form data from the post request to file
    file = request.files['file']

    if 'file' not in request.files:
        return jsonify({
            'error':'There is no file'
        })

    if file.filename == '':
        return jsonify({
            'error':'No selected file'
        })
    
    try:
        # preprocess uploaded img
        img_array = preprocess_image(file)
        print(img_array)
        
        # Make Predictions
        predictions = model.predict(img_array)
        class_index = np.argmax(predictions[0]) # Return the index of the cat and dog: cat= 0 , dog= 1

        if class_index == 0:
            result = 'Cat'
        else:
            result = 'Dog'    

        # Response of the post request
        return jsonify({
            'result':result
        })


    except Exception as e:
        return jsonify({
            'error' : str(e)
        })


if __name__ == '__main__':
    app.run(debug=True)  




