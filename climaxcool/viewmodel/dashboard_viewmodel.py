from flask import render_template, request
from climaxcool.models import Users, Customers, Equipments, Services
from climaxcool.repository.repo_customers import Repo_Customers
from climaxcool.forms import FormNewService
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


repo_customers = Repo_Customers()

class Dashboard_ViewModel():

    def dashboard(self):
        customers = [];
        return render_template('dashboard.html', customers=customers, type_data='')


    def dashboard_customers(self):
        name = request.args.get('name_customer_input');
        print(name);

        if name:
            customers = Customers.query.filter(Customers.name_customer.ilike(f'%{name}%')).all();
        elif name != None:
            customers = Customers.query.order_by(Customers.name_customer).all();
        else:
            customers = [];     

        return render_template('dashboard.html', customers=customers, type_data='clientes')    


    def dashboard_users(self):
        name = request.args.get('name_customer_input');
        print(name);

        if name:
            customers = Users.query.filter(Users.username.ilike(f'%{name}%')).all();
        elif name != None:
            customers = Users.query.order_by(Users.username).all();
        else:
            customers = [];     

        return render_template('dashboard.html', customers=customers, type_data='usuarios')   