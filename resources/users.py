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
        login_user(created_user)
        created_user_dict = model_to_dict(created_user)
        created_user_dict.pop('password')
        return jsonify(data=created_user_dict, message=f'succesffully created user {created_user.username}', status=200), 200



@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()

    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)
        user_dict.pop('password')
        password_good = check_password_hash(user.password, payload['password'])
        if password_good:
            login_user(user)
            return jsonify(data=user_dict, message='sucessfully logged in user', status=200), 200
        else:
            return jsonify(data={}, message='email or password incorrect', status=200), 200


    except models.DoesNotExist:
        return jsonify(data={}, message='email does not exist', status=200), 200


@users.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(data={}, message='successfully logged out user', status=200), 200