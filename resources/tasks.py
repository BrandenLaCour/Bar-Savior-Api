import models
from flask import request, jsonify, Blueprint
from flask_login import login_required, current_user

from playhouse.shortcuts import model_to_dict


tasks = Blueprint('tasks', 'tasks')

#Index route 
@tasks.route('/all', methods=['GET'])
def show_tasks():
    tasks = models.Task.select()
    tasks_dict = [model_to_dict(task) for task in tasks]
    return jsonify(data=tasks_dict, message='retrieved {} tasks'.format(len(tasks_dict)), status=200), 200


#Create route
@tasks.route('/', methods=['POST'])
@login_required
def create_task():
    payload= request.get_json()
    
    if current_user.admin:
        created_task = models.Task.create(**payload)
        created_task_dict = model_to_dict(created_task)
        return jsonify(data=created_task_dict, message=f'succesfully created task \"{created_task.name}\" ')

    else:
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200


@tasks.route('/<id>', methods=['Delete'])
@login_required
def delete(id):
    if current_user.admin:
        delete_query = models.Task.delete().where(models.Task.id == id)
        delete_query.execute()
        return jsonify(data={}, message='successfully deleted task at id {}'.format(id), status=200), 200
    else: 
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200