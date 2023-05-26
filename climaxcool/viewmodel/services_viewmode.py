from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user
from climaxcool.models import Users, Customers, Equipments, Services
from climaxcool.repository.repo_customers import Repo_Customers
from climaxcool.forms import FormNewService
from climaxcool import database
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


repo_customers = Repo_Customers()


class report_service_model:
    def __init__(self, id, date, list_services, annotations, expert, price):
        self.id = id
        self.date = date
        self.list_services = list_services
        self.annotations = annotations
        self.expert = expert
        self.price = price


class Services_ViewModel():

    def new_service(self, customer_id, equipment_id):
        form_new_service = FormNewService()
        form_new_service.expert.choices = [current_user.username]
        customer = Customers.query.filter_by(id=customer_id).first()
        equipment = Equipments.query.filter_by(id=equipment_id).first()
        text_services = ""

        #if permissão total pode escolher qualquer técnico
        #senão só tem a opção de escolher ele mesmo como técnico
        #criar essas condições após terminar authenticação e estrutura de permissões

        if current_user.is_authenticated and form_new_service.validate_on_submit():
            for service in form_new_service:
                if "service_" in service.name and service.data:
                    print(f"{service.data}  {service.name}  {service.label.text}")
                    text_services += service.label.text + ","
            if(len(text_services) > 1):
                new_service = Services(
                    service = text_services,
                    annotations = form_new_service.annotations.data,
                    price = form_new_service.price.data,
                    id_customer = customer_id,
                    id_equipment = equipment_id,
                    id_expert = current_user.id,
                )
                #Código para pegar o id gravado no DB, creio que não será necessário
                # new_service_id = new_service.id
                # print(new_service_id)
                database.session.add(new_service)
                database.session.commit()
                return redirect(url_for("report_service", equipment_id=equipment_id))
            else:
                pass
                    
        return render_template('new_service.html', form_new_service=form_new_service, customer=customer, equipment=equipment)
    

    def report_service(self, equipment_id):
        equipment = None
        services_for_equipment = []

        if equipment_id is not None:
            equipment = Equipments.query.filter_by(id=equipment_id).first()
            customer = Customers.query.filter_by(id=equipment.id_customer).first();
            services = Services.query.filter_by(id_equipment=equipment_id).all();

            for service in services:
                expert = Users.query.filter_by(id=service.id_expert).first();
                #Colocoar um delay neste ponto?
                list_services = service.service.split(",")
                list_services.pop()
                print(f"lista de serviços {list_services}")
                services_for_equipment.append( report_service_model(
                    id=service.id,
                    date= service.date_create,
                    list_services= list_services,
                    annotations= service.annotations,
                    expert= expert.username,
                    price= service.price,
                )) 

        return render_template('report_service.html', equipment=equipment, customer=customer, services=services_for_equipment)  