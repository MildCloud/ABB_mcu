from flask import Flask, request, jsonify, send_from_directory, json
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import ast
import json
import time
import RPi.GPIO as GPIO

import flask
import abb_mcu
current_app = abb_mcu.app

# SSR
# Set up GPIO
SSR_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SSR_PIN, GPIO.OUT)

# 初始化CORS
CORS(abb_mcu.app, resources={r"/*": {"origins": "*"}})


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



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
        GPIO.output(SSR_PIN, GPIO.HIGH)
    elif req_dict['require'] == 'off':
        GPIO.output(SSR_PIN, GPIO.LOW)
    return _corsify_actual_response(flask.jsonify({}))




    