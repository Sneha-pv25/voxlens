import os
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import librosa
import base64
from werkzeug.utils import secure_filename

# Initialize Flask application
app = Flask(__name__)

# Set up a model or load a pretrained model for AI-based detection (dummy for now)
model = None  # Replace with your actual model loading code

# Set up the allowed file extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'aac'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_model():
    """Load your AI model here (if necessary)."""
    global model
    if model is None:
        # Example: model = tf.keras.models.load_model('path_to_your_model')
        pass

def create_spectrogram(file_path):
    """Generate and return the spectrogram image from the audio file."""
    y, sr = librosa.load(file_path)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    
    # Create a figure
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    
    # Save the figure to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Convert the image to base64 for embedding in the HTML
    img_b64 = base64.b64encode(img.read()).decode('utf-8')
    return img_b64

@app.route('/')
def index():
    """Serve the index.html page."""
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    """Process the uploaded audio file and return a prediction."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        
        # Save the uploaded file
        file.save(file_path)

        # Process the file and get the prediction
        result = process_audio(file_path)

        # Create spectrogram image
        spectrogram_image = create_spectrogram(file_path)

        return jsonify({
            'success': True,
            'data': {
                'result': result,
                'spectrogram': spectrogram_image
            }
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

def process_audio(file_path):
    """Process the audio file and return a fake speech prediction result."""
    # Dummy logic for speech analysis (replace with your actual model logic)
    load_model()  # Load model if needed
    
    # Here you can use your model to predict the result
    # Example: prediction = model.predict(file_path)
    
    # Return a dummy result for now
    return 'Fake'  # or 'Real' based on the actual model

if __name__ == '__main__':
    # Ensure the uploads folder exists
    os.makedirs('uploads', exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True)
