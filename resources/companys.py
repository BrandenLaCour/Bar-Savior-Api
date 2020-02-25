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


#Create new company
@companys.route('/', methods=['POST'])
def create():
    payload = request.get_json()
    created_company = models.Company.create(**payload)
    created_company_dict = model_to_dict(created_company)

    return jsonify(data=created_company_dict, message=f'successfully created company {created_company.name}', status=200), 200

#Delete route, MUST make login required, and current_user must be 'master'
@companys.route('/<id>', methods=['Delete'])
@login_required
def delete(id):
    delete_query = models.Company.delete().where(models.Company.id == id)
    delete_query.execute()

    return jsonify(data={}, message=f"successfully deleted company with id of {id}", status=200),200

#Update route, need to get auth working then only master user can do this.
@companys.route('/<id>', methods=['PUT'])
@login_required
def update(id):
    payload = request.get_json()
    update_query = models.Company.update(**payload).where(models.Company.id == id)
    updated_company = models.Company.get_by_id(id)
    
    return jsonify(data={}, message=f'succesfully update company {updated_company.name}', status=200),200