from flask import Blueprint, jsonify, request
import models


companys = Blueprint('companys', 'companys')

@companys.route('/', methods=['GET'])
def hello_world():
    return 'hellow world companys'