from flask import request, send_file
from flask_login import login_user, logout_user, current_user, login_required
from flask_restful import Resource, reqparse, fields, marshal_with, marshal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from io import BytesIO
import json

from app import db
from app.models import *
from app.calculators import *
from app.pdf import *


class Users(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('login', required=True,
                                help='login for the new user')
            parser.add_argument('email', required=True,
                                help='email address for the new user')
            parser.add_argument('password', required=True,
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
        parser.add_argument('login', required=True,
                            help='login for the user')
        parser.add_argument('password', required=True,
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


def invoice_args(req=None):
    parser = reqparse.RequestParser()

    parser.add_argument('customer_name', required=True,
                        help='customer name')
    parser.add_argument('customer_tax_id', required=False,
                        help='legal ID')
    parser.add_argument('customer_contact_person', required=False,
                        help='name of the contact person')
    parser.add_argument('customer_email', required=False,
                        help='email address')
    parser.add_argument('customer_invoicing_address', required=True,
                        help='address to be used for invoicing')
    parser.add_argument('customer_shipping_address', required=True,
                        help='address to be used for shipping')
    parser.add_argument('notes',
                        help='invoice specific notes')

    return parser.parse_args(req)


class InvoicesList(Resource):
    _fields = {
        'id': fields.Integer,
        'ref_num': fields.Integer,
        'customer_name': fields.String,
        'issued_on': fields.DateTime(dt_format='iso8601'),
        'due_on': fields.DateTime(dt_format='iso8601'),
        'sent_on': fields.DateTime(dt_format='iso8601'),
        'paid_on': fields.DateTime(dt_format='iso8601'),
    }

    @login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int,
                            help='page number')
        parser.add_argument('count', type=int,
                            help='page size')
        parser.add_argument('sorting', type=json.loads,
                            help='sorting fields with order')
        args = parser.parse_args()

        totalQuery = Invoice.query.filter_by(owner_id=current_user.get_id())
        query = totalQuery

        # sorting param
        if args['sorting'] is not None:
            for name, direction in args['sorting'].items():
                # sanitize by looking up fields/directions in models
                fieldobj = getattr(Invoice, name)
                dirobj = getattr(fieldobj, direction)()
                query = query.order_by(dirobj)

        # paging params
        if all(args[p] is not None for p in ('count', 'page')):
            query = query.limit(
                args['count']).offset(
                    (args['page']-1) * args['count'])

        return {'items': marshal(query.all(), InvoicesList._fields),
                'totalItemCount': totalQuery.count()}

    @login_required
    def post(self):
        try:
            args = invoice_args(request)

            invoice = Invoice(
                owner_id=current_user.get_id(),
                ref_num=current_user.make_next_invoice_number(),
                **args)

            db.session.add(invoice)
            db.session.commit()

            return {'message': 'invoice created', 'id': invoice.id}
        except IntegrityError:
            return {'message': 'invoice already exists'}, 409


class Invoices(Resource):
    _fields = {
        'id': fields.Integer,
        'ref_num': fields.Integer,
        'issued_on': fields.DateTime(dt_format='iso8601'),
        'due_on': fields.DateTime(dt_format='iso8601'),
        'delivered_on': fields.DateTime(dt_format='iso8601'),
        'sent_on': fields.DateTime(dt_format='iso8601'),
        'paid_on': fields.DateTime(dt_format='iso8601'),
        'po_num': fields.String,
        'notes': fields.String,
        'customer_name': fields.String,
        'customer_tax_id': fields.String,
        'customer_contact_person': fields.String,
        'customer_email': fields.String,
        'customer_invoicing_address': fields.String,
        'customer_shipping_address': fields.String,
    }

    _linefields = {
        'id': fields.Integer,
        'description': fields.String,
        'quantity': fields.Fixed(2),
        'unit': fields.String,
        'unit_price': fields.Fixed(2),
        'tax_rate': fields.Fixed(2),
        'currency': fields.String,
        'net_value': fields.Fixed(2),
    }

    _totalfields = {
        'net': fields.Fixed(2),
        'tax': fields.Fixed(2),
        'gross': fields.Fixed(2),
    }

    @login_required
    def get(self, id):
        try:
            invoice = marshal(Invoice.query.filter_by(
                owner_id=current_user.get_id(), id=id).one(),
                Invoices._fields)

            invoice['lines'] = marshal(
                list(map(LineCalculator().calculate,
                    InvoiceLine.query.filter_by(
                        invoice_id=id).all())),
                Invoices._linefields)

            total_calculator = TotalCalculator()
            (subtotals, total) = total_calculator.calculate(invoice['lines'])

            invoice['subtotals'] = {}
            for r, s in subtotals.items():
                invoice['subtotals'][r] = marshal(s, Invoices._totalfields)

            invoice['total'] = marshal(total, Invoices._totalfields)

            return invoice
        except NoResultFound:
            return {'message': 'invoice not found'}, 404

    @login_required
    def delete(self, id):
        try:
            invoice = Invoice.query.filter_by(
                owner_id=current_user.get_id(), id=id).one()

            db.session.delete(invoice)
            db.session.commit()

            return {'message': 'invoice removed'}
        except NoResultFound:
            return {'message': 'invoice not found'}, 404

    @login_required
    def put(self, id):
        try:
            args = invoice_args(request)

            invoice = Invoice.query.filter_by(
                owner_id=current_user.get_id(), id=id).one()

            # update model fields from args
            for k in args:
                setattr(invoice, k, args[k])

            db.session.commit()

            return {'message': 'invoice updated'}
        except NoResultFound:
            return {'message': 'invoice not found'}, 404


def customer_args(req=None):
    parser = reqparse.RequestParser()

    parser.add_argument('name', required=True,
                        help='customer name')
    parser.add_argument('tax_id', required=False,
                        help='legal ID')
    parser.add_argument('contact_person', required=False,
                        help='name of the contact person')
    parser.add_argument('email', required=False,
                        help='email address')
    parser.add_argument('invoicing_address', required=True,
                        help='address to be used for invoicing')
    parser.add_argument('shipping_address', required=True,
                        help='address to be used for shipping')
    return parser.parse_args(req)


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

    @login_required
    def post(self):
        try:
            args = customer_args(request)

            customer = Customer(user_id=current_user.get_id(), **args)

            db.session.add(customer)
            db.session.commit()

            return {'message': 'customer created', 'id': customer.id}
        except IntegrityError:
            return {'message': 'customer already exists'}, 409


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
        try:
            return Customer.query.filter_by(
                user_id=current_user.get_id(), id=id).one()
        except NoResultFound:
            return {'message': 'customer not found'}, 404

    @login_required
    def delete(self, id):
        try:
            customer = Customer.query.filter_by(
                user_id=current_user.get_id(), id=id).one()

            db.session.delete(customer)
            db.session.commit()

            return {'message': 'customer removed'}
        except NoResultFound:
            return {'message': 'customer not found'}, 404

    @login_required
    def put(self, id):
        try:
            args = customer_args(request)

            customer = Customer.query.filter_by(
                user_id=current_user.get_id(), id=id).one()

            # update model fields from args
            for k in args:
                setattr(customer, k, args[k])

            db.session.commit()

            return {'message': 'customer updated'}
        except NoResultFound:
            return {'message': 'customer not found'}, 404


class Calculator(Resource):
    def post(self):
        lines = []
        reqdata = request.get_json()
        calculator = LineCalculator()
        for l in reqdata['lines']:
            # use original state for unsaved lines
            if 'org' in l:
                l = l['org']
            line = marshal(
                calculator.calculate(InvoiceLine.from_dict(l)),
                Invoices._linefields
            )
            lines.append(line)

        total_calculator = TotalCalculator()
        (subtotals, total) = total_calculator.calculate(lines)

        for r, s in subtotals.items():
            subtotals[r] = marshal(s, Invoices._totalfields)

        total = marshal(total, Invoices._totalfields)

        return {'lines': lines, 'subtotals': subtotals, 'total': total}


class Exporter(Resource):
    def post(self):
        invoice = request.get_json()

        for l in invoice['lines']:
            if l['tax_rate'] is not None:
                invoice['has_tax'] = True
            # TODO: move to invoice model
            invoice['currency'] = l['currency']

        data = {'invoice': invoice, 'user': current_user}
        return send_file(BytesIO(export_pdf('pdf.html', data)),
                         mimetype='application/pdf',
                         as_attachment=True,
                         attachment_filename='%s.pdf' % invoice['ref_num'])
