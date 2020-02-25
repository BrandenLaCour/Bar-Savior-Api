import models
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user
from flask_bcrypt import check_password_hash, generate_password_hash

from playhouse.shortcuts import model_to_dict


users = Blueprint('users', 'users')


@users.route('/', methods=['Get'])
def hello_world():
    return 'users hello world'

@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, message='email already exists', status=200), 200


    except models.DoesNotExist:
        created_user = models.User.create(**payload)
        created_user.password = generate_password_hash(payload['password'])
        created_user.save()
        created_user_dict = model_to_dict(created_user)
        created_user_dict.pop('password')
        return jsonify(data=created_user_dict, message=f'succesffully created user {created_user.username}', status=200), 200