from flask import url_for, redirect, flash
from climaxcool.models import Users
from climaxcool import database
from sqlalchemy.exc import SQLAlchemyError

class Repo_Users():
    
    def save_user():
        pass
    
    def get_user_by_id(self, customer_id):
        user = Users.query.get(int(customer_id))
        return user
    
    def get_users_order_by_name(self):
        users = Users.query.order_by(Users.name_customer).all();
        return users

    def get_user_filter_by(self, selected_customer):
        user = Users.query.filter_by(name_customer=selected_customer).first();
        return user 

    def commit_update_user(self, msg_sucess, msg_fail):
        try:
            #ATUALIZAR date_last_update
            database.session.commit()
            flash(f'{msg_sucess}', 'alert-success')
            return redirect(url_for('dashboard_users'))
            
        except SQLAlchemyError as e:
            database.session.rollback()
            flash(f'{msg_fail}', 'alert-danger')

    def delete_user_by_id(self):
        pass