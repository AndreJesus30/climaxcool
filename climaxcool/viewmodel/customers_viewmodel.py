from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user
from climaxcool.models import Users, Customers
from climaxcool.repository.repo_customers import Repo_Customers
from climaxcool.forms import FormUsersRegistration, FormCustomerRegistration
from climaxcool import database
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


repo_customers = Repo_Customers()

class Customers_ViewModel():

    def customers_registration(self):
        form_customer = FormCustomerRegistration()

        if form_customer.validate_on_submit():
            print('formulário validado')
            new_customer = Customers(
                type_customer= form_customer.type_customer.data,
                number_register_customer= form_customer.number_register_customer.data,
                name_customer= form_customer.name_customer.data,
                name_responsible= form_customer.name_responsible.data,
                email= form_customer.email.data,
                address= form_customer.address.data,
                telephone_fixed= form_customer.telephone_fixed.data,
                telephone_mobile= form_customer.telephone_mobile.data,
                reference_point= form_customer.reference_point.data,
                id_user= current_user.id
            )
            database.session.add(new_customer)
            database.session.commit()
            print('salvo no banco de dados')
            flash('Cliente cadastrado com sucesso', 'alert-success'),
            return redirect(url_for('dashboard_customers'))
        return render_template('customer_registration.html', form_customer=form_customer)



    def customers_update(self, customer_id):
        customer = repo_customers.get_customer_by_id(customer_id)

        form_customer = FormCustomerRegistration(
            type_customer= customer.type_customer,
            number_register_customer= customer.number_register_customer,
            name_customer= customer.name_customer,
            name_responsible= customer.name_responsible,
            email= customer.email,
            address= customer.address,
            telephone_fixed= customer.telephone_fixed,
            telephone_mobile= customer.telephone_mobile,
            reference_point= customer.reference_point,
            status_customer= customer.status_customer
            )
        
        form_customer.edit_mode.data = 'True'

        if form_customer.validate_on_submit():
            print('form_validado')
            customer.number_register_customer=form_customer.number_register_customer.data
            customer.type_customer=form_customer.type_customer.data
            customer.number_register_customer=form_customer.number_register_customer.data
            customer.name_customer=form_customer.name_customer.data
            customer.name_responsible=form_customer.name_responsible.data
            customer.email=form_customer.email.data
            customer.address=form_customer.address.data
            customer.telephone_fixed=form_customer.telephone_fixed.data
            customer.telephone_mobile=form_customer.telephone_mobile.data
            customer.reference_point= form_customer.reference_point.data
            customer.status_customer= form_customer.status_customer.data
            customer.id_user= current_user.id
            customer.date_last_update= datetime.utcnow()

            try:
                database.session.commit()
                flash('Cliente editado com sucesso.', 'alert-success')
                return redirect(url_for('dashboard_customers'))
            
            except SQLAlchemyError as e:
                database.session.rollback()
                flash('Houve um problema na edição, verifique os dados e tente novamenteeee.', 'alert-danger')

        if form_customer.errors:
            print(form_customer.errors)
        

        return render_template('customer_update.html', form_customer=form_customer)
    

    def customer_change_status(self, customer_id):
        customer = repo_customers.get_customer_by_id(customer_id)

        if customer and customer.status_customer == "ATIVO":
            customer.status_customer = "INATIVO"
            repo_customers.commit_update_customer('Status alterado com sucesso', 'Houve um erro ao tentar alterar o status')
            return redirect(url_for('dashboard_customers'))
        
        else:
            customer.status_customer = "ATIVO"
            repo_customers.commit_update_customer('Status alterado com sucesso', 'Houve um erro ao tentar alterar o status')
            return redirect(url_for('dashboard_customers'))     