import datetime
from sqlalchemy.schema import ForeignKey, UniqueConstraint

from app import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(63), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, login, email, password, admin=False):
        self.login = login
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
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
    ref_num = db.Column(db.Integer, nullable=False)
    issued_on = db.Column(db.DateTime, nullable=False)
    due_on = db.Column(db.DateTime, nullable=False)


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
    __table_args__ = (
        UniqueConstraint('user_id', 'name'),
        UniqueConstraint('user_id', 'tax_id'),
    )

    def __init__(self, user_id, name, tax_id, contact_person,
                 email, invoicing_address, shipping_address):
        self.user_id = user_id
        self.name = name
        self.tax_id = tax_id
        self.contact_person = contact_person
        self.email = email
        self.invoicing_address = invoicing_address
        self.shipping_address = shipping_address
