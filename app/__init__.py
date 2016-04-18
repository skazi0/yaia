from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_restful import Api

from app.config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
app.config.from_envvar('YAIA_CONFIG')

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from app.models import *
from app.resources import *

api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


api.add_resource(Users, '/api/users')
api.add_resource(Sessions, '/api/sessions')
api.add_resource(Invoices, '/api/invoices')
api.add_resource(CustomersList, '/api/customers')
api.add_resource(Customers, '/api/customers/<id>')


@app.route('/')
def index():
    return app.send_static_file('views/index.html')
