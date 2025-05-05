from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from model.detector import predict_image # Import your prediction function

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads' # Directory to save uploaded files
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'} # Add video extensions if supported

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Determine if it's an image or video and process accordingly
        if filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
            prediction, confidence = predict_image(filepath)
            os.remove(filepath) # Clean up the uploaded file
            return jsonify({'prediction': prediction, 'confidence': confidence})
        elif filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov'}:
            # Implement video processing logic here
            # This might involve extracting frames, processing them, and aggregating results
            os.remove(filepath) # Clean up
            return jsonify({'error': 'Video processing not yet implemented'}), 501
        else:
            os.remove(filepath)
            return jsonify({'error': 'Unsupported file type'}), 400

    return jsonify({'error': 'Something went wrong'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') # Run the Flask app9