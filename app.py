import pyuac
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

@app.route('/upload-image', methods=['OPTIONS', 'POST'])
def upload_image():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'success'}), 200

    try:
        data = request.json.get("image")  # Get image data from the request
        if data:
            # Decode the Base64 image, removing the prefix
            image_data = base64.b64decode(data.split(",")[1])  # This splits off "data:image/png;base64,"

            # Create the images directory if it doesn't exist
            image_directory = "images"
            os.makedirs(image_directory, exist_ok=True)

            # Create a filename with the current timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"captured_image_{timestamp}.png"
            filepath = os.path.join(image_directory, filename)

            # Save the image file
            with open(filepath, "wb") as f:
                f.write(image_data)

            print(f"Image successfully saved at: {filepath}")  # Debug output
            return jsonify({"status": "success", "filename": filename})

        else:
            return jsonify({"status": "error", "message": "No image data received"}), 400

    except Exception as e:
        # Handle exceptions and print the error message
        print(f"Failed to decode and save image: {str(e)}")  # Debug output
        return jsonify({"status": "error", "message": f"Failed to save image: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
