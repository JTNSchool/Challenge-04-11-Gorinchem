import pyuac
import analyse

if not pyuac.isUserAdmin():
    pyuac.runAsAdmin()
    exit()

from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

IMAGE_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'images')
os.makedirs(IMAGE_FOLDER, exist_ok=True)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    data = request.json.get("image")
    if data:
        try:
            # Decode the Base64 image (strip prefix if present)
            image_data = base64.b64decode(data.split(",")[1])

            # Create a filename with the current timestamp
            filename = f"captured_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(IMAGE_FOLDER, filename)

            # Save the image file
            with open(filepath, "wb") as f:
                f.write(image_data)

            result = analyse.start(image_data)
            
            return jsonify({"status": "success", "filename": filename, "result": result})

        except (IndexError, ValueError, base64.binascii.Error) as e:
            # Handle any Base64 decoding errors
            return jsonify({"status": "error", "message": "Failed to decode image data"}), 400

    return jsonify({"status": "error", "message": "No image data provided"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
