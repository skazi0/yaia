from datetime import datetime
from decimal import Decimal
from sqlalchemy import func
from sqlalchemy.schema import ForeignKey, UniqueConstraint

from app import db, bcrypt


class Series(db.Model):

    __tablename__ = "series"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    prefix = db.Column(db.String(16), nullable=False, default='')
    next_invoice_num = db.Column(db.Integer, nullable=False, default=1)

    def make_next_invoice_number(self):
        num = self.next_invoice_num
        self.next_invoice_num += 1

        return num


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(63), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    address = db.Column(db.Text, nullable=False)
    tax_id = db.Column(db.String(63))

    def __init__(self, login, email, password, admin=False):
        self.login = login
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.now()
        self.admin = admin

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.login)


class Invoice(db.Model):

    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    series_id = db.Column(db.Integer, ForeignKey('series.id'), nullable=False)
    series_prefix = db.Column(db.String(16), nullable=False, default='')
    ref_num = db.Column(db.Integer, nullable=False)
    issued_on = db.Column(db.DateTime, nullable=False, default=func.now())
    due_on = db.Column(db.DateTime, nullable=False, default=func.now())
    delivered_on = db.Column(db.DateTime, nullable=False, default=func.now())
    sent_on = db.Column(db.DateTime)
    paid_on = db.Column(db.DateTime)
    notes = db.Column(db.Text, nullable=False, default='')
    po_num = db.Column(db.String(63))

    customer_name = db.Column(db.String(255), nullable=False)
    customer_tax_id = db.Column(db.String(63))
    customer_contact_person = db.Column(db.String(127))
    customer_email = db.Column(db.String(127))
    customer_invoicing_address = db.Column(db.Text, nullable=False)
    customer_shipping_address = db.Column(db.Text, nullable=False)


class InvoiceLine(db.Model):

    __tablename__ = "lines"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.Integer, ForeignKey('invoices.id'),
                           nullable=False)
    description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Numeric(12, 2), nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    # net_value = db.Column(db.Numeric(12, 2), nullable=False)
    tax_rate = db.Column(db.Numeric(5, 2))
    # value = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    is_prepaid = db.Column(db.Boolean, default=False, nullable=False)

    @staticmethod
    def from_dict(data):
        line = InvoiceLine()
        for k, v in data.items():
            if hasattr(line, k):
                if (v is not None and
                   isinstance(getattr(InvoiceLine, k).type, db.Numeric)):
                    v = Decimal(v)
                setattr(line, k, v)
        return line


class Customer(db.Model):

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    tax_id = db.Column(db.String(63))
    contact_person = db.Column(db.String(127))
    email = db.Column(db.String(127))
    invoicing_address = db.Column(db.Text, nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    __table_args__ = (
        UniqueConstraint('user_id', 'name'),
        UniqueConstraint('user_id', 'tax_id'),
    )

    def __init__(self, user_id, name, tax_id, contact_person,
                 email, invoicing_address, shipping_address, notes):
        self.user_id = user_id
        self.name = name
        self.tax_id = tax_id
        self.contact_person = contact_person
        self.email = email
        self.invoicing_address = invoicing_address
        self.shipping_address = shipping_address
        self.notes = notes
