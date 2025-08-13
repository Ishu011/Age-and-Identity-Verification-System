
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  
from tensorflow.keras.layers.experimental import LocallyConnected2D
from tensorflow.python.util import module_wrapper
import tensorflow.keras.layers

setattr(tensorflow.keras.layers, 'LocallyConnected2D', LocallyConnected2D)




from flask import Flask, render_template, request

from PIL import Image
import pytesseract
import re
from datetime import datetime
import cv2
from deepface import DeepFace
import base64
from io import BytesIO



app = Flask(__name__)
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_dob_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    dob_match = re.search(r'(\d{2}[-/]\d{2}[-/]\d{4})', text)
    if dob_match:
        return dob_match.group(1)
    year_match = re.search(r'\b(19|20)\d{2}\b', text)
    return year_match.group(0) if year_match else "DOB not found"

def detect_and_crop_face(image_path, output_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return False
    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        cv2.imwrite(output_path, face)
        return True
    return False

def calculate_age(dob_string):
    formats = ["%d/%m/%Y", "%d-%m-%Y", "%Y"]
    for fmt in formats:
        try:
            dob = datetime.strptime(dob_string, fmt)
            today = datetime.today()
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        except:
            continue
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id_img = request.files['id_card']
        selfie_data = request.form['selfie_data']

        if id_img and selfie_data:
            id_path = os.path.join(app.config['UPLOAD_FOLDER'], "id.jpg")
            selfie_path = os.path.join(app.config['UPLOAD_FOLDER'], "selfie.jpg")
            id_img.save(id_path)

            # Decode selfie
            selfie_data_clean = selfie_data.split(",")[1]
            selfie_image = Image.open(BytesIO(base64.b64decode(selfie_data_clean)))
            selfie_image.save(selfie_path)

            # OCR + DOB + Age
            dob = extract_dob_from_image(id_path)
            age = calculate_age(dob)

            # Face crop from ID
            id_face_path = os.path.join(app.config['UPLOAD_FOLDER'], "id_face.jpg")
            if not detect_and_crop_face(id_path, id_face_path):
                return render_template("index.html", result="Face not detected in ID card.", match_percent=None)

            # DeepFace match
            result = DeepFace.verify(img1_path=id_face_path, img2_path=selfie_path)
            match_percent = round(result["distance"], 2)
            match_score = max(0, round((1 - result["distance"]) * 100, 2))  # Convert distance to score

            selfie_base64 = "data:image/jpeg;base64," + base64.b64encode(open(selfie_path, "rb").read()).decode()

            if result["verified"]:
                if age is not None and age >= 18:
                    return render_template("index.html",
                                           result=f"Identity Verified (Match: {match_score}%). Age: {age} (18+)",
                                           match_percent=match_score,
                                           selfie_base64=selfie_base64)
                elif age is not None:
                    return render_template("index.html",
                                           result=f"Face Match (Match: {match_score}%), but underage. Age: {age}",
                                           match_percent=match_score,
                                           selfie_base64=selfie_base64)
                else:
                    return render_template("index.html",
                                           result=f"Face Match ({match_score}%), but DOB not found.",
                                           match_percent=match_score,
                                           selfie_base64=selfie_base64)
            else:
                return render_template("index.html",
                                       result=f"Face does not match. Match Score: {match_score}%",
                                       match_percent=match_score,
                                       selfie_base64=selfie_base64)

    # For GET requests
    return render_template("index.html", result="", match_percent=None, selfie_base64=None)

if __name__ == '__main__':
    app.run(debug=True)
