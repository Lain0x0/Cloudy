from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS

# Imgur API client ID
API_CLIENT_ID = "4f45e12ce00ec3c"
# Directories
UPLOAD_FOLDER = '/uploads/file.json'

# Configure the application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the 'uploads' directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_json_response(data, filename):
    try:
        # Define the full path where the JSON file should be saved
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Read existing data from the file, if it exists
        existing_data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_data = json.load(file)

        # Update the existing data with the new Imgur link
        existing_data.update(data)

        # Save the updated data back to the file
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)

        print(f"Successfully saved JSON response to {file_path}")

    except Exception as e:
        print(f"Error saving JSON response: {e}")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)
            print(f"File saved to {filepath}")

            with open(filepath, 'rb') as image_file:
                response = requests.post(
                    'https://api.imgur.com/3/image',
                    headers={'Authorization': f'Client-ID {API_CLIENT_ID}'},
                    files={'image': image_file}
                )

            os.remove(filepath)
            print(f"File removed from {filepath}")

            if response.status_code == 200:
                imgur_link = response.json()['data']['link']
                
                # Save the Imgur link to the JSON file at the specified path
                save_json_response({'imgur_link': imgur_link}, 'file.json')

                return jsonify({'link': imgur_link})
            else:
                return jsonify({'error': response.json()['data']['error']}), 500

        except Exception as e:
            print(f"Error processing file: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    else:
        return jsonify({'error': 'No file uploaded'}), 400

if __name__ == '__main__':
    app.run(port=5000)
