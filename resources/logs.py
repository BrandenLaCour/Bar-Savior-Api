import models
from flask import request, jsonify, Blueprint
from flask_login import login_required, current_user

from playhouse.shortcuts import model_to_dict


logs = Blueprint('logs', 'logs')

#all except the show have to be admin to crud

# Index route 
@logs.route('/all', methods=['GET'])
@login_required
def show_log():
    logs = models.Log.select()
    logs_dict = [model_to_dict(logs) for logs in logs]
    return jsonify(data=logs_dict, message='retrieved {} logs'.format(len(logs_dict)), status=200), 200

# #Show route
@logs.route('/<id>', methods=['GET'])
@login_required
def show_logs(id):
    logs = models.Log.get_by_id(id)
    logs_dict = model_to_dict(logs)
    return jsonify(data=logs_dict, message='retrieved logs {}'.format(logs.taskId.name), status=200),200


#Create route
@logs.route('/', methods=['POST'])
@login_required
def create_logs():
    payload= request.get_json()
    
    if current_user.admin:
        created_log = models.Log.create(**payload)
        created_log_dict = model_to_dict(created_log)
        return jsonify(data=created_log_dict, message=f'succesfully created log for \"{created_log.task.name}\" ')

    else:
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200

#Update logs (May not need)
@logs.route('/<id>', methods=["PUT"])
@login_required
def update_logs(id):
    payload = request.get_json()
    if current_user.admin:
        update_query = models.Log.update(**payload).where(models.Log.id == id)
        update_query.execute()
        updated_logs = models.Log.get_by_id(id)
        updated_logs_dict = model_to_dict(updated_logs)
        return jsonify(data=updated_logs_dict, message=f'successfully updated logs with id of {id}', status=200 ), 200
    else:
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200



#Delete Route
@logs.route('/<id>', methods=['Delete'])
@login_required
def delete(id):
    if current_user.admin:
        delete_query = models.Log.delete().where(models.Log.id == id)
        delete_query.execute()
        return jsonify(data={}, message='successfully deleted logs at id {}'.format(id), status=200), 200
    else: 
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200