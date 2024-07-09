"""ABBMCU package initializer."""

import flask

app = flask.Flask(__name__)

app.config.from_object('abb_mcu.config')

app.config.from_envvar('abb_mcu', silent=True)
import abb_mcu.model
import abb_mcu.views
