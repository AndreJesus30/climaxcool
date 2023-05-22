from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = '0bd6c52d8f78992ae8af1358bd38ff76'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///climaxcoolmanagement.db'

database = SQLAlchemy(app)
#bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'É necessário fazer login para continuar.'
login_manager.login_message_category = 'alert-info'

# with app.app_context():
#     database.create_all()

from climaxcool.route import routes
