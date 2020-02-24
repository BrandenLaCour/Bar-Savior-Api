import models
from flask import Blueprint, request, jsonify



users = Blueprint('users', 'users')



@users.route('/', methods=['Get'])
def hello_world():
    return 'users hello world'