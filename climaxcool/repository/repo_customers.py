from climaxcool.models import Customers
from flask import url_for, redirect, flash
from climaxcool import database
from sqlalchemy.exc import SQLAlchemyError

class Repo_Customers():
    
    def save_customer():
        pass
    
    def get_customer_by_id(self, customer_id):
        customer = Customers.query.get(int(customer_id))
        return customer
    
    def get_customers_order_by_name(self):
        customers = Customers.query.order_by(Customers.name_customer).all();
        return customers

    def get_customers_filter_by(self, selected_customer):
        customer = Customers.query.filter_by(name_customer=selected_customer).first();
        return customer 


    def commit_update_customer(self, msg_sucess, msg_fail):
        try:
            #ATUALIZAR date_last_update
            database.session.commit()
            flash(f'{msg_sucess}', 'alert-success')
            return redirect(url_for('dashboard_customers'))
            
        except SQLAlchemyError as e:
            database.session.rollback()
            flash(f'{msg_fail}', 'alert-danger')


    def delete_customer_by_id():
        pass
