from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# from flask_bcrypt import Bcrypt
# from flask_login import LoginManagers

app = Flask(__name__)

app.config['SECRET_KEY'] = '0bd6c52d8f78992ae8af1358bd38ff76'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///climaxcoolmanagement.db'

database = SQLAlchemy(app)

# with app.app_context():
#     database.create_all()

from climaxcool.route import routes
