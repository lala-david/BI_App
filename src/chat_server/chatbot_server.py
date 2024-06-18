from flask import Flask, request, jsonify
import os
import json
from threading import Lock

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
file_lock = Lock()

@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if not isinstance(data, dict) and not isinstance(data, list):
        return jsonify({"error": "Data should be a dictionary or a list of dictionaries"}), 400
    
    json_file_path = os.path.join(UPLOAD_FOLDER, 'temperature.json')

    try:
        with file_lock:
            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"success": "Data received", "file": json_file_path}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
