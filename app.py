import os
import models
from flask import Flask, Blueprint, jsonify, request
from resources.members import members
from resources.companys import companys
from resources.rooms import rooms
from resources.tasks import tasks
from resources.logs import logs
from flask_login import LoginManager
from flask_cors import CORS


PORT = 8000
DEBUG = True


app = Flask(__name__)
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True


app.secret_key = 'my secret key'  
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.Member.get(models.Member.id == userid)
    except models.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(data={'error': 'user has not logged in'}, message='you must login to access that resource', status=401), 401


CORS(members, origins=['http://localhost:3000', 'https://bar-savior-app.herokuapp.com'], supports_credentials=True)
CORS(companys, origins=['http://localhost:3000', 'https://bar-savior-app.herokuapp.com'], supports_credentials=True)
CORS(rooms, origins=['http://localhost:3000', 'https://bar-savior-app.herokuapp.com'], supports_credentials=True)
CORS(tasks, origins=['http://localhost:3000', 'https://bar-savior-app.herokuapp.com'], supports_credentials=True)
CORS(logs, origins=['http://localhost:3000', 'https://bar-savior-app.herokuapp.com'], supports_credentials=True)
                                            
app.register_blueprint(members, url_prefix='/api/v1/members')
app.register_blueprint(companys, url_prefix='/api/v1/companys')
app.register_blueprint(rooms, url_prefix='/api/v1/rooms')
app.register_blueprint(tasks, url_prefix='/api/v1/tasks')
app.register_blueprint(logs, url_prefix='/api/v1/logs')

@app.route('/', methods=['GET'])
def hello_world():
    return 'hello world'


if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)