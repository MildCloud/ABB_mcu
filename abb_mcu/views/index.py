from flask import Flask, request, jsonify, send_from_directory, json
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import ast
import json

import flask
import abb_mcu
current_app = abb_mcu.app


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
    # TODO Add the code to toggle the real machine
    return _corsify_actual_response(flask.jsonify({}))
    