from flask import Flask, render_template, request
import os
import subprocess
import io
import os
from google.cloud import vision
from google.cloud.vision_v1 import types
import pandas as pd
from proto.marshal.collections.repeated import RepeatedComposite
import proto
import json
import numpy as np
from google.protobuf.json_format import MessageToJson
from google.cloud.vision_v1 import AnnotateImageResponse
from flask import Flask
from flask import request
from flask import render_template
import cv2
import imutils

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
file_path = None
f_p=""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        # Check if a file is provided in the request
        if 'file' not in request.files:
            return render_template('code_box.html',js_content="pp", error='No file provided')

        file = request.files['file']

        # Check if the file has a valid extension
        if file.filename == '' or not allowed_file(file.filename):
            return render_template('code_box.html',js_content="oo", error='Invalid file type')

        # Save the uploaded file
        f_p = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(f_p)
        print("poojita",f_p )

        # Process the image (you can replace this with your image processing function)
        # processed_output = process_image(file_path)

    # file_path = '/Users/Poojita/Desktop/Dolphin_Google_Vision_API_Test/code_file.js'
    # try:
    #     with open(file_path, 'r') as file:
    #         js_content = file.read()
    #     # Render the template with the processed output and JS content
    #         return render_template('code_box.html', js_content=js_content)
    # except Exception as e:
    # # Print or log the error for debugging
    #     print(f"Error reading file: {e}")
    # # Handle the error gracefully, e.g., return an error message to the user
    #     return render_template('code_box.html', error="Error reading file. Please try again.")
    return render_template('code_box.html')


@app.route('/run_script')
def run_script():
    global file_path  # Access the global variable
    print('File path in run_script:', file_path)  # Debugging statement
    if file_path is None:
        return 'File path is not set. Please set the file path first.'
    
    try:
        file_path_string = file_path
        result = subprocess.run(['python', '/Users/Poojita/Desktop/Dolphin_Google_Vision_API_Test/test_vision.py', file_path_string], check=True, capture_output=True, text=True)
        output = result.stdout
        return f'Python script executed successfully! Output: {output}'
    except subprocess.CalledProcessError as e:
        error_output = e.stderr
        return f'Error executing Python script: {e}. Error output: {error_output}'

@app.route('/process_image_path', methods=['POST'])
def process_image_path():
    global file_path  # Access the global variable
    try:
        file_path = request.json['file_path']
        print('Received file path:', file_path)  # Debugging statement
        return 'File path received'
    except KeyError:
        return 'Error: Missing file_path field in JSON request', 400  # Bad request status code


@app.route('/get_js_content', methods=['GET'])
def get_js_content():
    # Define the path to the JavaScript file
    file_path = '/Users/Poojita/Desktop/Dolphin_Google_Vision_API_Test/code_file.js'
    try:
        # Read the content of the JavaScript file
        with open(file_path, 'r') as file:
            js_content = file.read()
        # Render the template with the JavaScript content
        return js_content
    except Exception as e:
        # Print or log the error for debugging
        print(f"Error reading file: {e}")
        # Handle the error gracefully, e.g., return an error message to the user
        return e
if __name__ == '__main__':
    app.run(debug=True)
