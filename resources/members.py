import models
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash, generate_password_hash

from playhouse.shortcuts import model_to_dict


members = Blueprint('members', 'members')


@members.route('/', methods=['Get'])
def hello_world():
    
    return 'users hello world'

#Index Route
@members.route('/all/<companyid>', methods=['GET'])
@login_required
def show_users(companyid):
    users = models.Member.select().where(models.Member.company == companyid)
    users_dict = [model_to_dict(user) for user in users]
    users_no_pass = [user.pop('password') for user in users_dict]
    return jsonify(data=users_dict, message='retrieved {} users'.format(len(users_dict)), status=200),200


#Create User  (may need more authentication to make sure only admins can make users)
@members.route('/register', methods=['POST'])
def register():
    payload = request.get_json(force=True)

    try:
        models.User.get(models.Member.email == payload["email"])
        return jsonify(data={}, message='email already exists', status=401), 401


    except models.DoesNotExist:
       
        created_user = models.Member.create(**payload)
        created_user.password = generate_password_hash(payload['password'])
        created_user.save()
        created_user_dict = model_to_dict(created_user)
        created_user_dict.pop('password')

        if not current_user.is_authenticated:
            #only add user to current session if there is no user already in session
            login_user(created_user)
        return jsonify(data=created_user_dict, message=f'succesffully created user {created_user.username}', status=200), 200


#Login
@members.route('/login', methods=['POST'])
def login():
    payload = request.get_json(force=True)

    try:
        user_query = models.Member.get(models.Member.email == payload['email'])
        if user_query.active == True:
            user_dict = model_to_dict(user_query)
            user_dict.pop('password')
            password_good = check_password_hash(user_query.password, payload['password'])
            if password_good:
                login_user(user_query)
                return jsonify(data=user_dict, message='sucessfully logged in user', status=200), 200
            else:
                return jsonify(data={}, message='email or password incorrect', status=401), 401
        else:
            return jsonify(data={}, message='user deactivated', status=401), 401


    except models.DoesNotExist:
        return jsonify(data={}, message='email does not exist', status=401), 401

#Logout
@members.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify(data={}, message='successfully logged out user', status=200), 200

#Deactivate user route instead of delete
@members.route('/deactivate/<id>', methods=['PUT'])
@login_required
def deactivate(id):
    payload = request.get_json(force=True)
    
    if current_user.admin:
        update_query = models.Member.update(active=False).where(models.User.id == id)
        #harcoded for now, need to fix as payload doesnt give false for some reason
        update_query.execute()
        updated_user = models.Member.get_by_id(id)
        updated_user_dict = model_to_dict(updated_user)
        return jsonify(data=updated_user_dict, message='succesfully deactivated user {}'.format(updated_user.email), status=200), 200

    else:
        return jsonify(data={}, message="you don't have the access rights to do that", status=401), 401


#Update User
@members.route('/<id>', methods=['PUT'])
@login_required
def update(id):
    payload = request.get_json(force=True)
 
    #only update of user is admin
    if current_user.admin:
        update_query = models.Member.update(**payload).where(models.User.id == id)
        update_query.execute()
        updated_user = models.Member.get_by_id(id)
        updated_user_dict = model_to_dict(updated_user)
        return jsonify(data=updated_user_dict, message='succesfully update user {}'.format(updated_user.email), status=200), 200

    else:
        return jsonify(data={}, message="you don't have the access rights to do that", status=401), 401

#Delete Routes
@members.route('/<id>', methods=['Delete'])
@login_required
def delete(id):
    print(current_user.username)
    #delete if the current user is admin
    if current_user.admin:
        delete_query = models.Member.delete().where(models.User.id == id)
        delete_query.execute()
        return jsonify(data={}, message='sucessfully deleted user with id {}'.format(id), status=200), 200
    else:
        return jsonify(data={}, message="you don't have the access rights to do that", status=401), 401
