from flask.ext.login import login_user, logout_user, current_user, login_required
from flask_restful import Resource, reqparse, fields, marshal_with
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import *


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
        return {'authenticated': True,
                'id': current_user.get_id(),
                'login': current_user.login,
                'email': current_user.email}

    def anonymous_session(self):
        return {'authenticated': False,
                'id': None,
                'login': None,
                'email': None}

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
    _fields = {
        'id': fields.Integer,
        'ref_num': fields.Integer,
        'issued_on': fields.DateTime(dt_format='iso8601'),
    }

    @login_required
    @marshal_with(_fields)
    def get(self):
        return Invoice.query.filter_by(
            owner_id=current_user.get_id()).order_by(
                Invoice.issued_on.desc()).all()


class CustomersList(Resource):
    _fields = {
        'id': fields.Integer,
        'name': fields.String,
        'tax_id': fields.String,
    }

    @login_required
    @marshal_with(_fields)
    def get(self):
        return Customer.query.filter_by(user_id=current_user.get_id()).all()


class Customers(Resource):
    _fields = {
        'id': fields.Integer,
        'name': fields.String,
        'tax_id': fields.String,
        'contact_person': fields.String,
        'email': fields.String,
        'invoicing_address': fields.String,
        'shipping_address': fields.String,
    }

    @login_required
    @marshal_with(_fields)
    def get(self, id):
        return Customer.query.filter_by(user_id=current_user.get_id(), id=id).one()
