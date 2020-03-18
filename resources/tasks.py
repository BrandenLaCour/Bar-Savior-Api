import models
from flask import request, jsonify, Blueprint
from flask_login import login_required, current_user

from playhouse.shortcuts import model_to_dict


tasks = Blueprint('tasks', 'tasks')

#all except the show have to be admin to crud

#Index route 
@tasks.route('/all/<roomid>', methods=['GET'])
@login_required
def show_tasks(roomid):
    tasks = models.Task.select().where(models.Task.room == roomid)
    tasks_dict = [model_to_dict(task) for task in tasks]
    return jsonify(data=tasks_dict, message='retrieved {} tasks'.format(len(tasks_dict)), status=200), 200

#Show route
@tasks.route('/<id>', methods=['GET'])
@login_required
def show_task(id):
    task = models.Task.get_by_id(id)
    task_dict = model_to_dict(task)
    return jsonify(data=task_dict, message='retrieved task {}'.format(task.name), status=200),200



#Create route
@tasks.route('/', methods=['POST'])
@login_required
def create_task():
    payload= request.get_json(force=True)
    
    if current_user.admin:
        created_task = models.Task.create(**payload)
        created_task_dict = model_to_dict(created_task)
        return jsonify(data=created_task_dict, message=f'succesfully created task \"{created_task.name}\" ')

    else:
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200

#Update Task
@tasks.route('/<id>', methods=["PUT"])
@login_required
def update_task(id):
    payload = request.get_json(force=True)
    if current_user.admin:
        update_query = models.Task.update(**payload).where(models.Task.id == id)
        update_query.execute()
        updated_task = models.Task.get_by_id(id)
        updated_task_dict = model_to_dict(updated_task)
        return jsonify(data=updated_task_dict, message=f'successfully updated task with id of {id}', status=200 ), 200
    else:
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200



#Deactivate task
@tasks.route('/deactivate/<id>', methods=['PUT'])
@login_required
def deactivate(id):
    if current_user.admin:
        update_query = models.Task.update(active=False).where(models.Task.id == id).execute()
        updated_task = models.Task.get(models.Task.id == id)
        updated_task_dict = model_to_dict(updated_task)
        return jsonify(data=updated_task_dict, message='successfully deactivated task at id {}'.format(id), status=200), 200
    else: 
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200