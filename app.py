from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from config import *
from utils import *
import logging
from flask_cors import CORS

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/predict', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({
            "status": {"code": 400, "message": "error, no file part!"}
        }), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            "status": {"code": 400, "message": "error, no selected file!"}
        }), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            image = crop_pupil(file_path)
            result = cataract_prediction(image)
            return jsonify({
                "status": {"code": 201, "message": "Success uploading the image!"},
                "result": result
            }), 200
        except Exception as e:
            logging.error(f"Error processing image: {str(e)}")
            return jsonify({
                "status": {"code": 500, "message": "Error processing the image!"}
            }), 500

    return jsonify({"status": {"code": 400, "message": "Invalid file type"}}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)