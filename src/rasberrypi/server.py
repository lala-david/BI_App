from flask import Flask, jsonify
import serial
from threading import Thread, Lock, Timer
from datetime import datetime
import json
import os
import time
import requests

app = Flask(__name__)

serial_config = {
    'temp_humidity': {'port': '/dev/ttyACM3', 'baud': 9600},
    'mq_sensors': {'port': '/dev/ttyACM2', 'baud': 115200},
    'dust_sensor': {'port': '/dev/ttyACM1', 'baud': 9600},
    'mq135': {'port': '/dev/ttyACM0', 'baud': 9600}
}

json_file_path = "data/Temperature.json"

latest_data = {
    'temperature': 0.0,
    'humidity': 0.0,
    'mq2_ppm': 0.0,
    'mq7_ppm': 0.0,
    'dust_density': 0.0,
    'air_quality': 'Unknown',
    'mq135_ppm': 0.0,
    'timestamp': ''  # Initialize the timestamp key
}

data_lock = Lock()

def init_serial(port, baud_rate):
    try:
        ser = serial.Serial(port, baud_rate)
        print(f"Connected to {port} at {baud_rate} baud.")
        return ser
    except serial.SerialException:
        print(f"Error: Could not open serial port {port}.")
        return None

def update_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def read_temp_humidity_data(ser):
    global latest_data
    while True:
        if ser and ser.in_waiting > 0:
            data_str = ser.readline().decode('utf-8').rstrip()
            temp, humi = data_str.replace("temp:", "").replace("humi:", "").split()
            with data_lock:
                latest_data.update({
                    'temperature': float(temp),
                    'humidity': float(humi),
                    'timestamp': update_timestamp()  # Update timestamp
                })
                update_json(json_file_path, latest_data)

def read_mq_data(ser):
    global latest_data
    while True:
        if ser and ser.in_waiting > 0:
            data_str = ser.readline().decode('utf-8').rstrip()
            sensor_type, ppm_value = data_str.split(": ")
            ppm = float(ppm_value.split(" ")[0])
            with data_lock:
                if "MQ-2" in sensor_type:
                    latest_data['mq2_ppm'] = ppm
                elif "MQ-7" in sensor_type:
                    latest_data['mq7_ppm'] = ppm
                latest_data['timestamp'] = update_timestamp()  # Update timestamp
                update_json(json_file_path, latest_data)

def read_dust_data(ser):
    global latest_data
    while True:
        if ser and ser.in_waiting > 0:
            data_str = ser.readline().decode('utf-8').rstrip()
            try:
                if "Dust Density:" in data_str and "-" in data_str:
                    dust_density_str, quality_str = data_str.split(" - ")
                    dust_density_val = float(dust_density_str.split(": ")[1])
                    air_quality_val = quality_str.split(": ")[1]
                    
                    with data_lock:
                        latest_data.update({
                            "dust_density": dust_density_val,
                            "air_quality": air_quality_val,
                            "timestamp": update_timestamp()  # Update timestamp
                        })
                        update_json(json_file_path, latest_data)
                else:
                    print(f"Unexpected format for dust sensor data: {data_str}")
            except ValueError as e:
                print(f"Error converting dust sensor data to float. Data: {data_str}, Error: {e}")
            except IndexError as e:
                print(f"Data format error in dust sensor data: {data_str}, Error: {e}")
            except Exception as e:
                print(f"General error reading dust sensor data: {e}")

def read_mq135_data(ser):
    global latest_data
    while True:
        if ser and ser.in_waiting > 0:
            data_str = ser.readline().decode('utf-8').rstrip()
            try:
                if ':' in data_str:
                    ppm_value = data_str.split(": ")[1]
                    ppm = float(ppm_value)
                    with data_lock:
                        latest_data.update({
                            'mq135_ppm': ppm,
                            'timestamp': update_timestamp()  # Update timestamp
                        })
                        update_json(json_file_path, latest_data)
                else:
                    print(f"Unexpected format for MQ-135 data: {data_str}")
            except ValueError as e:
                print(f"Error converting MQ-135 data to float. Data: {data_str}, Error: {e}")
            except IndexError as e:
                print(f"Data format error in MQ-135 data: {data_str}, Error: {e}")
            except Exception as e:
                print(f"General error reading MQ-135 data: {e}")

for key, config in serial_config.items():
    ser = init_serial(config['port'], config['baud'])
    if ser:
        if key == 'temp_humidity':
            Thread(target=read_temp_humidity_data, args=(ser,), daemon=True).start()
        elif key == 'mq_sensors':
            Thread(target=read_mq_data, args=(ser,), daemon=True).start()
        elif key == 'dust_sensor':
            Thread(target=read_dust_data, args=(ser,), daemon=True).start()
        elif key == 'mq135':
            Thread(target=read_mq135_data, args=(ser,), daemon=True).start()

def timed_data_send():
    Timer(10.0, timed_data_send).start()
    send_data_to_server(json_file_path)

data_file_lock = Lock()

def update_json(path, data):
    with data_file_lock:
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)

def send_data_to_server(file_path, endpoint='http://../upload'):
    with data_file_lock:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(endpoint, json=data, headers=headers)
                    print(f"Response from server: {response.text}")
                except requests.RequestException as e:
                    print(f"Failed to send data: {e}")
                except json.JSONDecodeError as e:
                    print(f"JSON decoding error: {e}")

@app.route('/data', methods=['GET'])
def get_data():
    with data_lock:
        return jsonify(latest_data)

if __name__ == '__main__':
    timed_data_send()
    app.run(host='0.0.0.0', port=8000)