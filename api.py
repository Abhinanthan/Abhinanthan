import shutil
import cv2
import os
import numpy as np
from PIL import Image, ImageEnhance
from qreader import QReader
import json
import base64
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

# Ensure the 'uploads' directory exists
def ensure_upload_dir():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    return UPLOAD_FOLDER

# Delete the 'uploads' directory and its contents
def delete_upload_dir():
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)

# Save images from request
def save_images_from_request(request):
    upload_folder = ensure_upload_dir()
    files = request.files.getlist('images')
    saved_files = []

    for file in files:
        if file.filename == '':
            return "One of the selected files has no filename", 400

        filename = file.filename
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        saved_files.append(file_path)

    return saved_files, 200

# Resize image to a maximum size
def resize_image(image_path, max_size=(800, 800)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size, Image.LANCZOS)
        img.save(image_path)

# Convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
        base64_encoded = base64.b64encode(image_data).decode("utf-8")
    return base64_encoded

# Send JSON data to another API
def send_data_to_api(json_data, api_url):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, data=json.dumps(json_data), headers=headers)
    return response.status_code, response.text

@app.route('/post', methods=['POST'])
def receive_data():
    saved_files, status_code = save_images_from_request(request)
    if status_code != 200:
        return saved_files, status_code

    response_data = []
    for file_path in saved_files:
        resize_image(file_path)
        base64_image = image_to_base64(file_path)

        # Process saved images for QR code detection
        qr_data = scan_qr_code(file_path)
        if not qr_data:
            preprocessed_path = preprocess_image(file_path)
            qr_data = scan_qr_code(preprocessed_path)
            if not qr_data:
                qr_data = fallback_qr_reader(file_path)

            if os.path.exists(preprocessed_path):
                os.remove(preprocessed_path)

        if qr_data:
            parts = qr_data.split(',')
            if len(parts) == 2:
                ufise_no, dc_no = parts
                data = {
                    "base64_image": base64_image,
                    "UDISE_code": ufise_no,
                    "DC_no": dc_no
                       }
                print(data)
                response_data.append(data)
            else:
                ufise_no = dc_no = None
                data = {
                    "base64_image": base64_image,
                    "UDISE_code": ufise_no,
                    "DC_no": dc_no
                       }
                print(data)
                response_data.append(data)
        else:
            ufise_no = dc_no = None
            data = {
                "base64_image": base64_image,
                "UDISE_code": ufise_no,
                "DC_no": dc_no
            }
            print(data)
            response_data.append(data)

    api_url = os.getenv('API_URL', 'http://192.168.50.72:5001/receive')
    status_code, response_text = send_data_to_api(response_data, api_url)

    delete_upload_dir()
    return jsonify(response_data), 200

def preprocess_image(image_path):
    image = Image.open(image_path).convert('L')
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    open_cv_image = np.array(image)
    open_cv_image = cv2.GaussianBlur(open_cv_image, (5, 5), 0)
    open_cv_image = cv2.adaptiveThreshold(open_cv_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    open_cv_image = cv2.filter2D(open_cv_image, -1, kernel)
    preprocessed_path = "preprocessed_image.png"
    cv2.imwrite(preprocessed_path, open_cv_image)
    return preprocessed_path

def scan_qr_code(image_path):
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, vertices_array, _ = detector.detectAndDecode(img)
    return data

def fallback_qr_reader(image_path):
    detector = QReader()
    img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    data = detector.detect_and_decode(image=img)
    return data

# Ensure the upload folder exists
ensure_upload_dir()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
