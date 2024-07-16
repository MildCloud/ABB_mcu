from flask import Flask, request, jsonify
from flask_cors import CORS
import RPi.GPIO as GPIO
import json
import time
import struct
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import pymodbus.constants as cst

from .. import app as current_app

# Initialize CORS with specific configurations
CORS(current_app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type", "Access-Control-Allow-Headers", "Authorization", "X-Requested-With"])

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    return response

# Set up GPIO
SSR_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SSR_PIN, GPIO.OUT)

@current_app.route('/toggle', methods=['POST', 'OPTIONS'])
def handle_toggle():
    if request.method == 'OPTIONS':
        return _corsify_actual_response(jsonify({}))

    req_dict_str = request.data.decode("UTF-8")
    req_dict = json.loads(req_dict_str)
    print('toggle require', req_dict['require'])

    if req_dict['require'] == 'on':
        GPIO.output(SSR_PIN, GPIO.HIGH)
    elif req_dict['require'] == 'off':
        GPIO.output(SSR_PIN, GPIO.LOW)

    return _corsify_actual_response(jsonify({}))

# Add similar CORS handling for other endpoints as needed


# Power Monitor
# Configure the serial connection
EN_485 = 4
GPIO.setup(EN_485, GPIO.OUT)
GPIO.output(EN_485, GPIO.LOW)

client = ModbusClient(
    method='rtu',
    port='/dev/ttyAMA0',  # Adjust the port name as necessary
    baudrate=9600,
    timeout=1,
    stopbits=1,
    bytesize=8,
    parity='N'
)

# Connect to the client
connection = client.connect()
if not connection:
    print("Failed to connect to the serial port")
    exit()

# Read the values from the specified registers
start_address = 0x0E
number_of_registers = 6
unit_id = 1  # Slave address

read_values = client.read_holding_registers(start_address, number_of_registers, unit=unit_id)

# Check if the read was successful and print the values
if not read_values.isError():
    print("Read values:", read_values.registers)
else:
    print("Error reading values")

# Close the connection
client.close()

@abb_mcu.app.route('/monitor', methods=['GET'])
def handle_monitor():
    # Read power data from the Sfere DDS1946-1P power meter
    ser.write(b'<command_to_request_data>')  # Replace with actual command
    time.sleep(1)
    power_data = ser.read(ser.in_waiting).decode('utf-8')
    
    # Parse the power data (example, adjust based on actual data format)
    power_data_dict = {'power': power_data}
    
    return _corsify_actual_response(flask.jsonify(power_data_dict))

# @abb_mcu.app.route('/toggle', methods=['POST'])
# def handle_toggle():
#     req_dict_str = request.data.decode("UTF-8")
#     req_dict = json.loads(req_dict_str)
#     print('toggle require', req_dict['require'])
#     # TODO Add the code to toggle the real machine
#     return _corsify_actual_response(flask.jsonify({}))
    
# @abb_mcu.app.route('/monitor', methods=['GET'])
# def handle_monitor():
#     # TODO Return Real Monitor Data here
#     monito_data = {'data1': 1, 'data2': 2}
#     return _corsify_actual_response(flask.jsonify(monito_data))