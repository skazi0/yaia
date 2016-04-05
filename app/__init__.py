from flask import Flask, request, jsonify
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from app.config import BaseConfig

# config

app = Flask(__name__)
app.config.from_object(BaseConfig)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from app.models import User

login_manager = LoginManager()
login_manager.init_app(app)

# skz: how to handle this with angular?
#login_manager.login_view = 'login'

#@login_manager.user_loader
#def load_user(id):
#    return User.query.get(int(id))

# routes

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/users', methods=['POST'])
def register():
    data = request.json
    try:
        user = User(login=data['login'],
                    email=data['email'],
                    password=data['password'])
    except:
        status = 'error parsing request'
        code = 400
    else:
        try:
            db.session.add(user)
            db.session.commit()
            status = 'OK'
            code = 200
        except:
            status = 'error creating user'
            code = 400
        db.session.close()

    return jsonify(result=status), code

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    pass
