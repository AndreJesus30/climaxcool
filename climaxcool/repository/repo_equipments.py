from climaxcool.models import Customers, Equipments
from flask import url_for, redirect, flash, request
from climaxcool import database
from sqlalchemy.exc import SQLAlchemyError

class Repo_Equipments():

    def save_equipment(self):
        pass
    

    def get_equipment_by_id(self, equipment_id):
        equipment = Equipments.query.get(int(equipment_id))
        return equipment
    

    def get_equipments_order_by_name(self):
        equipments = Equipments.query.order_by(Equipments.name_equipment).all();
        return equipments


    def get_equipments_filter_by(self, selected_equipment):
        equipment = Equipments.query.filter_by(name_equipment=selected_equipment).first();
        return equipment 


    def commit_update_equipment(self,customer_id, msg_sucess, msg_fail):
        try:
            #ATUALIZAR date_last_update
            database.session.commit()
            flash(f'{msg_sucess}', 'alert-success')
            # return redirect(url_for('equipment_summary', customer_id=customer_id))
            
        except SQLAlchemyError as e:
            database.session.rollback()
            print(e)
            flash(f'{msg_fail}', 'alert-danger')


    def delete_equipment_by_id():
        pass