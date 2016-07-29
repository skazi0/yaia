from flask import Flask, render_template
from flask.ext.bower import Bower
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_restful import Api

from app.config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
app.config.from_envvar('YAIA_CONFIG')

bower = Bower(app)
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
api.add_resource(InvoicesList, '/api/invoices')
api.add_resource(Invoices, '/api/invoices/<id>')
api.add_resource(CustomersList, '/api/customers')
api.add_resource(Customers, '/api/customers/<id>')
api.add_resource(Calculator, '/api/calculator')
api.add_resource(Exporter, '/api/export')

@app.route('/')
def index():
    return render_template('index.html')
