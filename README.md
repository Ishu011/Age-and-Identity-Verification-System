# Age and Identity Verification System

This project is a complete age and identity verification solution developed using Python, Flask, DeepFace, OpenCV, and Tesseract OCR. It allows users to upload a government-issued ID (such as Aadhaar) and capture a live selfie using their webcam. The system performs Optical Character Recognition (OCR) to extract the date of birth (DOB), calculates the user’s age, detects and compares facial features between the ID and the selfie, and then verifies if the user is 18 years or older.

### WorkFlow:
![alt text](image-1.png)

## Features

### 1. Face Verification
- Compares the face detected in the uploaded ID card against the face in the captured selfie.
- Uses DeepFace for robust face recognition.
- Returns a verification result along with a confidence score.

### 2. Age Detection
- Automatically extracts the date of birth from the ID card using Tesseract OCR.
- Calculates the user's current age.
- Verifies whether the user is 18 years or older.


### 3. Blurry Image Detection
- Detects poor quality or blurry selfies using OpenCV’s Laplacian Variance method.
- Notifies the user if the image quality is insufficient for accurate detection.

### 4. OCR Support
- Enables DOB detection from Aadhaar and other local ID formats.

### 5. Real-time Selfie Capture and Image Display
- Allows users to take a live selfie directly from the browser.
- Displays both the ID card and the captured selfie side-by-side after submission.

### 6. User Interface
- Clean and professional UI built with HTML, CSS, and JavaScript.
- Provides immediate feedback including face match score, age detection, and verification result.


##  Folder Structure

```
Age and Identity Verification System/
├── backend/
│   ├── app.py               # Flask application backend
│   ├── requirements.txt     # Python dependencies
│   ├── templates/
│   │   └── index.html       # Frontend HTML page
│   ├── static/
│   │   ├── style.css        # CSS styling
│   │   └── uploads/         # Folder to save uploaded ID and selfie images
├── README.md                # Project documentation

```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Tesseract OCR installed on your system

### Step 1: Clone the Repository

git clone https://github.com/Ishu011/Age-and-Identity-Verification-System.git

### Step 2: Create Virtual Environment 
### Step 3: Install Required Python Packages
### Step 4: Install Tesseract OCR
Download and install from: https://github.com/tesseract-ocr/tesseract
### Running the Application
In the terminal, run the Flask application : python app.py

### How the System Works : 
1. Upload ID Card: User uploads a scanned or photographed copy of a government-issued ID.
2. Capture Selfie: User captures a real-time selfie using the camera.
3. OCR Extraction: System extracts text from the ID card image and searches for DOB.
4. Face Detection and Cropping: System detects and crops the face region from the ID card.
5. Face Matching: Compares the cropped ID face with the live selfie using DeepFace.
6. Blurry Detection: Detects if the selfie is too blurry to be used.
7. Verification Result: Displays:
8. Whether the user is verified
9. Age detected
10. Confidence percentage for face match

### Dependencies
The system uses the following Python libraries:
1. Flask
2. Pillow
3. pytesseract
4. OpenCV (opencv-python)
5. DeepFace
6. numpy

### Future Improvements
-Add OCR support for additional regional languages.
-Add backend image encryption before temporary storage.
-Support PAN, voter ID and passport formats.
-OTP or email-based verification as a second factor.
-Deploy to cloud platforms (e.g., Render, Heroku, Azure).

### Contributing
If you'd like to contribute to this project, then fork the repository, make changes, and submit a pull request.

