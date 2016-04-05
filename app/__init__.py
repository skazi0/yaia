from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_restful import Resource, Api, reqparse
from sqlalchemy.exc import IntegrityError

from app.config import BaseConfig

# config

app = Flask(__name__)
app.config.from_object(BaseConfig)

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from app.models import User

# skz: how to handle this with angular?
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def load_user(id):
#    return User.query.get(int(id))

# routes


@app.route('/')
def index():
    return app.send_static_file('index.html')


class Users(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('login', type=str, required=True,
                                help='login for the new user')
            parser.add_argument('email', type=str, required=True,
                                help='email address for the new user')
            parser.add_argument('password', type=str, required=True,
                                help='password for the new user')
            args = parser.parse_args()

            user = User(login=args['login'],
                        email=args['email'],
                        password=args['password'])

            db.session.add(user)
            db.session.commit()
            db.session.close()

            return {'message': 'user created'}
        except IntegrityError:
            return {'message': 'user already exists'}, 400


api.add_resource(Users, '/api/users')


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    pass
