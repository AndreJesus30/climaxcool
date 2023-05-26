from flask import render_template, url_for, redirect, request, flash, abort
from climaxcool.models import Users, Customers, Services, Equipments
from climaxcool.forms import FormUsersRegistration
from climaxcool import database
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from climaxcool.repository.repo_customers import Repo_Customers
from climaxcool.repository.repo_users import Repo_Users


repo_customers = Repo_Customers()
repo_uers = Repo_Users()

class User_ViewModel():

    def users_registration(self):
        form_users = FormUsersRegistration()
        customers = repo_customers.get_customers_order_by_name()

        if form_users.validate_on_submit():
            print('formulário validado')
            selected_customer = request.form.get('selected_customer')
            print(f'cliente selecionado {selected_customer}')
            customer = repo_customers.get_customers_filter_by(selected_customer) #Customers.query.filter_by(name_customer=selected_customer).first();
            print(f'customer {customer}')
            if customer:
                new_user = Users(
                    type_user=form_users.type_user.data,
                    username=form_users.username.data, 
                    email= "sememail@email.com" if not form_users.email.data else form_users.email.data,
                    password=form_users.password.data,
                    permission_user= 0 if not form_users.permission_user.data else form_users.permission_user.data,
                    id_customer= customer.id
                )
                database.session.add(new_user)
                database.session.commit()
                flash(f'Usuário {form_users.username.data} criado com sucesso', 'alert-success')
                print('salvo no banco de dados')
                return redirect(url_for('dashboard_users'))
            else:
                flash(f'Cliente {selected_customer} não existe no sistema', 'alert-danger')
                print('Não foi salvo no banco de dados')

        if form_users.errors:
            print(form_users.errors)        

        return render_template('users_registration.html', form_users=form_users, customers=customers)
    

    def user_update(self, user_id):
        user = Users.query.get(int(user_id))

        form_user = FormUsersRegistration(
            type_user = user.type_user,
            username=user.username, 
            email= user.email,
            password=user.password,
            password_check=user.password,
            permission_user= user.permission_user,
            )
        
        form_user.edit_mode.data = 'True'

        if form_user.edit_mode.data:
            form_user.password.validators = []
            form_user.password_check.validators = []

        if form_user.validate_on_submit():
            print('form_validado')
            user.username=form_user.username.data 
            user.email= form_user.email.data
            user.password=form_user.password.data
            user.permission_user= form_user.permission_user.data
            user.status_user = form_user.status_user.data
            user.date_last_update= datetime.utcnow()

            try:
                database.session.commit()
                flash('Usuário editado com sucesso.', 'alert-success')
                return redirect(url_for('dashboard_users'))
            
            except SQLAlchemyError as e:
                database.session.rollback()
                flash('Houve um problema na edição, verifique os dados e tente novamente.', 'alert-danger')

        if form_user.errors:
            print(form_user.errors)
            

        return render_template('users_update.html', form_users=form_user)
    
    
    def user_delete(self, user_id):
        user = Users.query.get(int(user_id))

        if user and user.type_user == "Externo":
            try:
                database.session.delete(user)
                database.session.commit()
                flash(f'Usuário {user.username} deletado com sucesso.', 'alert-success')
                return redirect(url_for('dashboard_users'))
            
            except SQLAlchemyError as e:
                database.session.rollback()
                flash('Houve um problema ao tentar deletar, tente mais tarde ou entre em contato com o suporte', 'alert-danger')  

        elif user and user.type_user == "Funcionário":
            services = Services.query.filter_by(id_expert=user.id).first();
            if services:
                flash('Usuário possui registros no sistema, é possível apenas Inativá-lo', 'alert-danger')
                return redirect(url_for('dashboard_users'))
            elif not services:       
                customer = Customers.query.filter_by(id_user=user.id).first();
                if customer:
                    flash('Usuário possui registros no sistema, é possível apenas Inativá-lo', 'alert-danger') 
                    return redirect(url_for('dashboard_users'))
                elif not customer:
                    equipment = Equipments.query.filter_by(id_user=user.id).first();
                    if equipment:
                        flash('Usuário possui registros no sistema, é possível apenas Inativá-lo', 'alert-danger')
                        return redirect(url_for('dashboard_users'))
                    else:
                        try:
                            database.session.delete(user)
                            database.session.commit()
                            flash(f'Usuário {user.username} deletado com sucesso.', 'alert-success')
                            return redirect(url_for('dashboard_users'))
                        
                        except SQLAlchemyError as e:
                            database.session.rollback()
                            flash('Houve um problema ao tentar deletar, tente mais tarde ou entre em contato com o suporte', 'alert-danger')      
        else:
            abort('403')


    def user_reset_password(self, user_id):
        user = repo_uers.get_user_by_id(user_id)

        if user:
            user.password = "123456"  
            repo_uers.commit_update_user('Senha resetada com sucesso, nova senha: 123456', 'Houve um erro ao tentar resetar a senha')
            return redirect(url_for('dashboard_users'))
        

    def user_change_status(self, user_id):
        user = repo_uers.get_user_by_id(user_id)

        if user and user.status_user == "ATIVO":
            user.status_user = "INATIVO"
            repo_uers.commit_update_user('Status alterado com sucesso', 'Houve um erro ao tentar alterar o status')
            return redirect(url_for('dashboard_users'))
        
        else:
            user.status_user = "ATIVO"
            repo_uers.commit_update_user('Status alterado com sucesso', 'Houve um erro ao tentar alterar o status')
            return redirect(url_for('dashboard_users'))     