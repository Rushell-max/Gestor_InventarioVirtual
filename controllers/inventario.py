from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify

from flask_cors import CORS, cross_origin

from models.task_inventario import TaskObject

object_blueprint = Blueprint('object_blueprint', __name__)

model = TaskObject()


@object_blueprint.route('/object/create_object', methods=['POST'])
@cross_origin()
def create_object():
    content = model.create_object(request.json['name'], request.json['description'])
    return content


@object_blueprint.route('/object/get_objects', methods=['GET'])
@cross_origin()
def get_objects():
    return jsonify(model.get_objects())


@object_blueprint.route('/object/delete_object', methods=['DELETE'])
@cross_origin()
def delete_object():
    return jsonify(model.delete_object(int(request.json['id'])))