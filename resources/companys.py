from flask import Blueprint, jsonify, request
import models
from flask_login import current_user, login_required, current_user
from playhouse.shortcuts import model_to_dict

companys = Blueprint('companys', 'companys')

@companys.route('/', methods=['GET'])
@login_required
def hello_world():
    print('all is well')
    return 'hello world companys'

#Index Route
@companys.route('/all', methods=['GET'])
@login_required
def show_companys():
    companys = models.Company.select()
    companys_dict = [model_to_dict(company) for company in companys]
    return jsonify(data=companys_dict, message='retrieved {} companys'.format(len(companys_dict)), status=200),200



#Create new company
@companys.route('/', methods=['POST'])
def create():
    payload = request.get_json(force=True)
    print(f'the payload is {payload}')
    created_company = models.Company.create(**payload)
    created_company_dict = model_to_dict(created_company)

    return jsonify(data=created_company_dict, message=f'successfully created company {created_company.name}', status=200), 200

#Delete route,
@companys.route('/<id>', methods=['Delete'])
@login_required
def delete(id):
    #if current user is master user, allow delete, otherwise dont
    if (current_user.master):
        #destroy all data from company
        # subqueries to delete logs by the company. first gather all rooms by company, then do subqueries to see if logs, tasks, and rooms are inside that array, if so, delete them.

        companysRooms = models.Room.select().where(models.Room.company == id)
        delete_logs_query = models.Log.delete().where(models.Log.task.in_(companysRooms)).execute() 
        delete_tasks_query = models.Task.delete().where(models.Task.room.in_(companysRooms)).execute()
        delete_rooms = [room.delete_instance() for room in companysRooms]
        delete_users_query = models.User.delete().where(models.User.company == id).execute()
        delete_query = models.Company.delete().where(models.Company.id == id).execute()
 
        return jsonify(data={}, message=f"successfully destroyed company with id of {id}", status=200),200
    else: 
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200



#Update route,  **Need a Cascading Delete!!**
@companys.route('/<id>', methods=['PUT'])
@login_required
def update(id):
    #allow user to update company only if master user
    payload = request.get_json(force=True)
    if current_user.master:
        update_query = models.Company.update(**payload).where(models.Company.id == id)
        update_query.execute()
        updated_company = models.Company.get_by_id(id)
        return jsonify(data={}, message=f'succesfully update company {updated_company.name}', status=200),200
    else:
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200