from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import tensorflow as tf
import pickle
import os
from PIL import Image
import numpy as np

app = Flask(__name__)

# Load the model (using pickle)
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Create uploads directory if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

def preprocess_image(image_path):
    # Load image
    img = Image.open(image_path)
    
    # Resize image to match the input size of your model (example: 224x224)
    img = img.resize((224, 224))
    
    # Convert image to numpy array and normalize (e.g., scaling pixel values to [0, 1])
    img_array = np.array(img) / 255.0
    
    # Add batch dimension (model expects a batch of images)
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['image']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        # Preprocess the image
        image = preprocess_image(file_path)

        # Make prediction
        prediction = model.predict(image)

        # Convert prediction to a human-readable format
        result = "Pneumonia" if prediction[0][0] > 0.5 else "Normal"

        return jsonify({'result': result})

@app.route('/prediction', methods=['GET'])
def get_prediction():
    image_id = request.args.get('image_id')
    # Retrieve the image path from your database or temporary storage
    image_path = get_image_path(image_id) # type: ignore

    # Preprocess the image
    image = preprocess_image(image_path)

    # Make prediction
    prediction = model.predict(image)

    # Convert prediction to a human-readable format
    result = "Pneumonia" if prediction[0][0] > 0.5 else "Normal"

    return jsonify({'result': result})

if __name__ == '_main_':
    app.run(debug=True)