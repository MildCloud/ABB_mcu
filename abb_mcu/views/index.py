from flask import Flask, request, jsonify, send_from_directory, json
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import ast
import json
import time
import RPi.GPIO as GPIO

import serial
import struct
import modbus_tk.modbus_rtu as rtu
import modbus_tk.defines as cst

import flask
import abb_mcu
current_app = abb_mcu.app

# 初始化CORS
CORS(abb_mcu.app, resources={r"/*": {"origins": "*"}})

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# SSR
# Set up GPIO
EN_485 = 4
SSR_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SSR_PIN, GPIO.OUT)
GPIO.setup(EN_485, GPIO.OUT) # Use Pin 4 as output 
GPIO.output(EN_485, GPIO.LOW) # Set Pin 4 as LOW

# Set up the serial connection for Modbus RTU
ser = serial.Serial(port='/dev/ttyAMA0', baudrate=9600, parity="N")
if ser.isOpen():
    print("Serial Opened")
master = rtu.RtuMaster(ser)
master.set_timeout(1.0)
master.set_verbose(True)

@app.route('/monitor', methods=['GET'])
def handle_monitor():
    try:
        # Define Modbus transaction parameters
        slave_id = 195
        data_format = 0  # Assuming data_format is set to 0 for float

        # Read various sets of values based on the starting address and number of registers
        read_values_fwd = master.execute(slave_id, cst.HOLDING_REGISTERS, 0x000E, 2)
        read_values_bck = master.execute(slave_id, cst.HOLDING_REGISTERS, 0x0010, 2)
        read_values_v = master.execute(slave_id, cst.HOLDING_REGISTERS, 0x0000, 2)
        read_values_i = master.execute(slave_id, cst.HOLDING_REGISTERS, 0x0002, 2)

        # Convert register values to float
        float_value_fwd = convert_to_float(read_values_fwd[0], read_values_fwd[1])
        float_value_bck = convert_to_float(read_values_bck[0], read_values_bck[1])
        float_value_v = convert_to_float(read_values_v[0], read_values_v[1])
        float_value_i = convert_to_float(read_values_i[0], read_values_i[1])

        # Return the read power data
        power_data_dict = {
            'forward_power': float_value_fwd,
            'backward_power': float_value_bck,
            'voltage': float_value_v,
            'current': float_value_i
        }
        return _corsify_actual_response(jsonify(power_data_dict))

    except Exception as e:
        return _corsify_actual_response(jsonify({'error': str(e)}))

def convert_to_float(high, low):
    combined = (high << 16) + low
    float_value = struct.unpack('>f', struct.pack('>I', combined))[0]
    return float_value

def convert_to_long(values):
    combined = (values[0] << 48) + (values[1] << 32) + (values[2] << 16) + values[3]
    return combined

@abb_mcu.app.route('/monitor', methods=['GET'])
def handle_monitor():
    # TODO Return Real Monitor Data here
    monito_data = {'data1': 1, 'data2': 2}
    return _corsify_actual_response(flask.jsonify(monito_data))


@abb_mcu.app.route('/toggle', methods=['POST'])
def handle_toggle():
    req_dict_str = request.data.decode("UTF-8")
    req_dict = json.loads(req_dict_str)
    print('toggle require', req_dict['require'])

    if req_dict['require'] == 'on':
        GPIO.output(SSR_PIN, GPIO.HIGH) # Turn pin 17 on
    elif req_dict['require'] == 'off':
        GPIO.output(SSR_PIN, GPIO.LOW) # Turn pin 17 off
    return _corsify_actual_response(flask.jsonify({}))




    