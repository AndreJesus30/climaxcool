from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user
from climaxcool.models import Users, Customers, Equipments
from climaxcool.repository.repo_customers import Repo_Customers
from climaxcool.forms import FormEquipmentsRegistration
from climaxcool import database
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


repo_customers = Repo_Customers()

class Equipments_ViewModel():

    def equipments_registration(self, customer_id):
        
        #Cadastrando pela rota fora de uma empresa
        if customer_id is None:

            form_equipments = FormEquipmentsRegistration()
            customers = Customers.query.order_by(Customers.name_customer).all();
            form_equipments.customer.choices = [" "]
            form_equipments.customer.choices += [customer.name_customer for customer in customers]

            if form_equipments.validate_on_submit():
                name_customer = form_equipments.customer.data
                id_customer = Customers.query.filter_by(name_customer=name_customer).first().id;
                
                new_equipments = Equipments(
                    name_equipment= form_equipments.brand_equipment.data +" - "+ form_equipments.btus_equipment.data +" BTUs - "+form_equipments.address.data,
                    btus_equipment=form_equipments.btus_equipment.data,
                    brand_equipment=form_equipments.brand_equipment.data, 
                    address=form_equipments.address.data,
                    qr_code= None if not form_equipments.qr_code.data else form_equipments.qr_code.data,
                    id_customer= id_customer,
                    id_user=current_user.id,
                )
                database.session.add(new_equipments)
                database.session.commit()
                flash('Equipamento cadastrado com sucesso', 'alert-success')
                return redirect(url_for('dashboard_customers'))

        #Cadastrando pela rota dentro de uma empresa
        if customer_id:
            form_equipments = FormEquipmentsRegistration()
            customer = Customers.query.filter_by(id=customer_id).first();
            form_equipments.customer.choices = [customer.name_customer];
            form_equipments.customer.data = customer.name_customer;

            if form_equipments.validate_on_submit():
                
                new_equipments = Equipments(
                    name_equipment= form_equipments.brand_equipment.data +" - "+ form_equipments.btus_equipment.data +" BTUs - "+form_equipments.address.data,
                    btus_equipment=form_equipments.btus_equipment.data,
                    brand_equipment=form_equipments.brand_equipment.data, 
                    address=form_equipments.address.data,
                    qr_code= None if not form_equipments.qr_code.data else form_equipments.qr_code.data,
                    id_customer= customer_id,
                    id_user=current_user.id,
                )
                database.session.add(new_equipments)
                database.session.commit()
                return redirect(url_for('equipment_summary', customer_id=customer_id))
        
        return render_template('equipments_registration.html', form_equipments=form_equipments)
    

    def equipment_summary(self, customer_id):
        customer = Customers.query.filter_by(id=customer_id).first();
        equipments = Equipments.query.filter_by(id_customer=customer_id).all();
        print(equipments);

        return render_template('summary_equipments.html', customer=customer, equipments=equipments)


    def equipment_summary_filter(self, customer_id):
        customer = Customers.query.filter_by(id=customer_id).first();
        name_equipment = request.args.get('name_equipment_input');
        equipments_filter = [];
        
        if name_equipment:
            equipments = Equipments.query.filter_by(id_customer=customer_id).all();
            for i in equipments:
                if name_equipment.upper() in (i.name_equipment +" "+ i.address).upper():
                    equipments_filter.append(i)
        elif name_equipment != None:
            equipments_filter = Equipments.query.filter_by(id_customer=customer_id).all();
        else:
            equipments_filter = [];     

        return render_template('summary_equipments.html', customer=customer, equipments=equipments_filter)   
