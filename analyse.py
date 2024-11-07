import face_recognition
import os
import numpy as np
from io import BytesIO
from PIL import Image
import base64

# Path to the main directory containing subdirectories of images
DATABASE_PATH = 'images'

# Dictionary to hold face encodings and associated names
known_faces = {}

# Function to load images from the database and compute encodings
def load_database():
    for person_name in os.listdir(DATABASE_PATH):
        person_dir = os.path.join(DATABASE_PATH, person_name)
        
        # Check if it's a directory (folder for a person)
        if os.path.isdir(person_dir):
            for filename in os.listdir(person_dir):
                filepath = os.path.join(person_dir, filename)
                
                # Load each image file and get the face encodings
                image = face_recognition.load_image_file(filepath)
                encodings = face_recognition.face_encodings(image)
                
                # Only consider images with exactly one face
                if len(encodings) == 1:
                    if person_name not in known_faces:
                        known_faces[person_name] = []
                    known_faces[person_name].append(encodings[0])
                    print(f"Loaded face encoding for {person_name} from {filename}")
                else:
                    print(f"Skipping {filename} in {person_name}: found {len(encodings)} faces")

# Run this at startup to populate known faces from the database
load_database()

# Function to analyze an image and compare it to the database
def start(image_data):
    # If image_data is in base64, decode it
    if isinstance(image_data, str):
        image_data = base64.b64decode(image_data.split(",")[1])  # Remove "data:image/png;base64," if present
    
    # Convert the byte data to a PIL image
    image = Image.open(BytesIO(image_data))
    
    # Ensure the image is in RGB format
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert the PIL image to a numpy array for face_recognition
    image_np = np.array(image)
    
    # Get face encodings from the target image
    face_encodings = face_recognition.face_encodings(image_np)
    
    if not face_encodings:
        print("No faces found in the provided image.")
        return {"status": "error", "message": "No faces found."}

    # Loop through faces in the input image (in case there are multiple)
    results = []
    for encoding in face_encodings:
        # Compare with all known faces for each person
        match_found = False
        for person_name, encodings_list in known_faces.items():
            # Compare the face encoding with each encoding for this person
            matches = face_recognition.compare_faces(encodings_list, encoding)
            face_distances = face_recognition.face_distance(encodings_list, encoding)
            
            # If there's a match, return the name of the person with the closest match
            if any(matches):
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    results.append(person_name)
                    print(f"Match found: {person_name}")
                    match_found = True
                    break  # Stop searching if a match is found

        if not match_found:
            print("No match found for this face.")
            results.append("Unknown")

    return {"status": "success", "matches": results}