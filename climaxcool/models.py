from climaxcool import database
from datetime import datetime


class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    type_user = database.Column(database.String, nullable=False) 
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    status_user = database.Column(database.String, default="ATIVO")
    permission_user = database.Column(database.Integer, default=0)
    customer = database.relationship('Customer', backref='created_by_user', lazy=True)
    # criar regras de permissionamento, somente leitura, edição, gravação, exclusão, total 


class Customer(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    type_customer = database.Column(database.String, nullable=False)
    number_register_customer = database.Column(database.String, nullable=False, unique=True)
    name_customer = database.Column(database.String, nullable=False)
    name_responsible = database.Column(database.String)
    email = database.Column(database.String)
    address = database.Column(database.String)
    telephone_fixed = database.Column(database.Integer)
    telephone_mobile = database.Column(database.Integer, nullable=False)
    reference_point = database.Column(database.String)
    #status_customer = database.Column(database.String, default="ATIVO")
    date_create = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_user = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
