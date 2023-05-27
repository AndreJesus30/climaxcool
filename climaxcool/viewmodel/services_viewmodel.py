from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user
from climaxcool.models import Users, Customers, Equipments, Services
from climaxcool.forms import FormNewService
from climaxcool import database
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from climaxcool.repository.repo_customers import Repo_Customers
from climaxcool.repository.repo_equipments import Repo_Equipments


repo_customers = Repo_Customers()
repo_equipments = Repo_Equipments()


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


    def update_service(self, service_id, equipment_id, customer_id):

        customer = Customers.query.filter_by(id=customer_id).first()
        equipment = Equipments.query.filter_by(id=equipment_id).first()
        service_selected = Services.query.get(int(service_id))
        expert = Users.query.filter_by(id=service_selected.id_expert).first();
        text_services = ""

        list_services = service_selected.service

        service_map = {
            'service_installation': 'Instalação',
            'service_disassembly': 'Desmontagem',
            'service_preventive_maintenance': 'Manutenção Preventiva',
            'service_corrective_maintenance': 'Manutenção Corretiva',
            'service_chemical_maintenance': 'Manutenção Química',
            'service_filter_cleaning': 'Limpeza de Filtros',
            'service_drain_clearing': 'Desobstrução de Dreno',
            'service_gas_charging': 'Carga de Gás',
            'service_electronic_board_repair': 'Reparo na Placa Eletrônica',
            'service_capacitor_replacement': 'Troca de Capacitor',
            'service_internal_fan_mode_exchange': 'Troca do Modo Ventilador Interno',
            'service_external_fan_mode_exchange': 'Troca do Modo Ventilador Externo',
            'service_compressor_replacement': 'Troca do Compressor'
        }

        service_status = {service: service_map[service] in list_services for service in service_map}

        form_service = FormNewService(
            service_installation = service_status['service_installation'],
            service_disassembly = service_status['service_disassembly'],
            service_preventive_maintenance = service_status['service_preventive_maintenance'],
            service_corrective_maintenance = service_status['service_corrective_maintenance'],
            service_chemical_maintenance = service_status['service_chemical_maintenance'],
            service_filter_cleaning = service_status['service_filter_cleaning'],
            service_drain_clearing = service_status['service_drain_clearing'],
            service_gas_charging = service_status['service_gas_charging'],
            service_electronic_board_repair = service_status['service_electronic_board_repair'],
            service_capacitor_replacement = service_status['service_capacitor_replacement'],
            service_internal_fan_mode_exchange = service_status['service_internal_fan_mode_exchange'],
            service_external_fan_mode_exchange = service_status['service_external_fan_mode_exchange'],
            service_compressor_replacement = service_status['service_compressor_replacement'],
            annotations = service_selected.annotations,
            expert = expert.username,
            price = service_selected.price
        )
        
        form_service.expert.choices = [expert.username]

        if form_service.validate_on_submit():
            print("form validado")
            for service in form_service:
                if "service_" in service.name and service.data:
                    print(f"{service.data}  {service.name}  {service.label.text}")
                    text_services += service.label.text + ","
            if(len(text_services) > 1):
                print("maior que 1")
                print(f"text_services: {text_services}")
                print(service_selected)
                service_selected.service = text_services
                service_selected.annotations = form_service.annotations.data 
                service_selected.price = form_service.price.data
                
                try:
                    database.session.commit()
                    flash('Serviço editado com sucesso.', 'alert-success')
                    return redirect(url_for("report_service", equipment_id=equipment_id))
            
                except SQLAlchemyError as e:
                    database.session.rollback()
                    flash('Houve um problema na edição, verifique os dados e tente novamenteeee.', 'alert-danger')

            else:
                pass

        if form_service.errors:
            print(form_service.errors)
            return redirect(url_for("report_service", equipment_id=equipment_id))
            
        return render_template('update_service.html', form_service=form_service, customer=customer, equipment=equipment)  