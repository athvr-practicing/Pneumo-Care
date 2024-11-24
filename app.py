import os
from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the trained model
model_path = 'model.pkl'
model = pickle.load(open(model_path, 'rb'))

# Configure upload folder and allowed file extensions
UPLOAD_FOLDER = 'static/uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if a file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    """
    Preprocess the uploaded image to match the input shape for the model.
    Assumes the model takes 200x200 RGB images.
    """
    img = Image.open(image_path).convert('RGB')  # Convert to RGB
    img = img.resize((200, 200))  # Resize to 200x200, which is the expected input size
    img_array = np.array(img) / 255.0  # Normalize pixel values
    img_array = img_array.reshape(1, 200, 200, 3)  # Add batch and channel dimensions
    return img_array

@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    """
    Handle image uploads, preprocess the image,
    and return the prediction.
    """
    if 'xray' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['xray']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Preprocess the image
        try:
            processed_image = preprocess_image(file_path)
        except Exception as e:
            return jsonify({'error': 'Failed to process the image', 'details': str(e)}), 500

        # Get prediction
        try:
            prediction = model.predict(processed_image)
            result = "Pneumonia Detected" if prediction[0] == 1 else "No Pneumonia Detected"
        except Exception as e:
            return jsonify({'error': 'Model prediction failed', 'details': str(e)}), 500

        # Return the result
        return jsonify({'filename': filename, 'result': result}), 200

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
