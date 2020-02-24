from flask import Blueprint, jsonify, request
import models

from playhouse.shortcuts import model_to_dict

companys = Blueprint('companys', 'companys')

@companys.route('/', methods=['GET'])
def hello_world():
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
def delete(id):
    delete_query = models.Company.delete().where(models.Company.id == id)
    delete_query.execute()

    return jsonify(data={}, message=f"successfully deleted company with id of {id}", status=200),200
