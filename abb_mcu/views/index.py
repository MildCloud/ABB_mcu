from flask import Flask, request, jsonify, send_from_directory, json
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import ast
import json

import flask
import abb_mcu
current_app = abb_mcu.app

import RPi.GPIO as GPIO
import serial
import time


# 初始化CORS
CORS(abb_mcu.app, resources={r"/*": {"origins": "*"}})


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# Set up GPIO
SSR_PIN = 17  # Example GPIO pin number, adjust as needed
GPIO.setmode(GPIO.BCM)
GPIO.setup(SSR_PIN, GPIO.OUT)

# SSR
@abb_mcu.app.route('/toggle', methods=['POST'])
def handle_toggle():
    req_dict_str = request.data.decode("UTF-8")
    req_dict = json.loads(req_dict_str)
    print('toggle require', req_dict['require'])
    
    # Toggle the SSR based on the request
    if req_dict['require'] == 'on':
        GPIO.output(SSR_PIN, GPIO.HIGH)
    elif req_dict['require'] == 'off':
        GPIO.output(SSR_PIN, GPIO.LOW)
    
    return _corsify_actual_response(flask.jsonify({}))

# Power Monitor
# Initialize serial communication for power meter
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust the serial port and baud rate as needed

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