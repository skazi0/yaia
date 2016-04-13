from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask_restful import Resource, Api, reqparse
from sqlalchemy.exc import IntegrityError

from app.config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
app.config.from_envvar('YAIA_CONFIG')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


api = Api(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from app.models import User


# skz: how to handle this with angular?
# login_manager.login_view = 'login'


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
            return {'message': 'user already exists'}, 409


class Sessions(Resource):
    def user_session(self):
        return {'authenticated': True, 'login': current_user.login, 'email': current_user.email}

    def anonymous_session(self):
        return {'authenticated': False, 'login': None, 'email': None}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login', type=str, required=True,
                            help='login for the user')
        parser.add_argument('password', type=str, required=True,
                            help='password for the user')
        args = parser.parse_args()

        user = User.query.filter_by(login=args['login']).first()

        if user is not None and user.check_password(args['password']):
            login_user(user)
            return self.user_session()
        else:
            return self.anonymous_session(), 403

    @login_required
    def get(self):
        if current_user.get_id() is not None:
            return [self.user_session()]
        else:
            return [self.anonymous_session()]

    @login_required
    def delete(self):
        logout_user()
        return {'message': 'OK'}

class Invoices(Resource):
    @login_required
    def get(self):
        return [{'date': '2015-01-01', 'name': 'invoice1'},
                {'date': '2015-02-01', 'name': 'invoice2'},
                {'date': '2015-03-01', 'name': 'invoice3'},
                ]


api.add_resource(Users, '/api/users')
api.add_resource(Sessions, '/api/sessions')
api.add_resource(Invoices, '/api/invoices')


