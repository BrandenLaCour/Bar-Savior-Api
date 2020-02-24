from flask import Flask, Blueprint, jsonify
import models
from resources.users import users
from resources.companys import companys
from flask_login import LoginManager
from flask_cors import CORS

PORT = 8000
DEBUG = True


app = Flask(__name__)


app.secret_key = 'my secret key'  
login_manager = LoginManager()
login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(userId):
#     try:
#         return models.User.get
#     except: 



CORS(users, origins=['http://localhost:3000'], support_credentials=True)
CORS(companys, origins=['http://localhost:3000'], support_credentials=True)

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(companys, url_prefix='/api/v1/companys')


@app.route('/', methods=['GET'])
def hello_world():
    return 'hello world'




if __name__ == '__main__':
    models.intialize()
    app.run(debug=DEBUG, port=PORT)