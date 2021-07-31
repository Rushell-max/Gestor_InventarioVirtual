from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from flask import session

import requests
import jwt
from functools import wraps
from datetime import datetime, timedelta

from controllers.inventario import object_blueprint

app = Flask(__name__)

app.register_blueprint(object_blueprint)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
