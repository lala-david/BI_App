from flask import Flask, request, jsonify
from threading import Lock
import json
import os

app = Flask(__name__)

data_lock = Lock()
data_file = os.path.join(os.path.dirname(__file__), 'polo', 'polo_data.json')

if not os.path.exists(data_file):
    with open(data_file, 'w') as file:
        json.dump([], file)

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.json
    
    with data_lock:
        with open(data_file, 'r') as file:
            existing_data = json.load(file)
        
        existing_data.append(data)

        with open(data_file, 'w') as file:
            json.dump(existing_data, file, indent=4)
    
    return jsonify({"status": "success", "message": "Data received and stored."})

@app.route('/data', methods=['GET'])
def get_data():
    with data_lock:
        with open(data_file, 'r') as file:
            data = json.load(file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9500)
