from climaxcool import app
from flask import render_template, url_for, redirect, request, jsonify, flash, abort, Blueprint
from climaxcool.models import Users, Customers, Equipments, Services
from climaxcool.repository.repo_customers import Repo_Customers
from climaxcool.shared import generate_code
from climaxcool import database
from flask_login import login_user, logout_user, current_user, login_required
from climaxcool.viewmodel.customers_viewmodel import Customers_ViewModel
from climaxcool.viewmodel.dashboard_viewmodel import Dashboard_ViewModel
from climaxcool.viewmodel.equipments_viewmodel import Equipments_ViewModel
from climaxcool.viewmodel.login_viewmodel import Login_ViewModel
from climaxcool.viewmodel.services_viewmode import Services_ViewModel
from climaxcool.viewmodel.users_viewmodel import User_ViewModel


generate_qrcodes = 'Função Gerar QR Codes'
list_qrcodes = ['qr1', 'qr2', 'qr3', 'qr4', 'qr5', 'qr6',]
list_images = []


# @app.route('/gerador-qrcodes')
# def generateQrCode():
#     # teste_list_images = url_for('static', filename=f"images/img_{1}.jpg")
#     return render_template('generate_qrcode.html', list_qrcodes=list_qrcodes, generate_qrcodes=generate_qrcodes, list_images=list_images)


customers_viewmodel = Customers_ViewModel()
user_viewmodel = User_ViewModel()
equipments_viewmodel = Equipments_ViewModel()
services_viewmodel = Services_ViewModel()
dashboard_viewmodel = Dashboard_ViewModel()
login_viewmodel = Login_ViewModel()


### HOME


@app.route('/')
def home():
    return render_template('home.html')


### LOGIN


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = login_viewmodel.login()
    return login


@app.route('/sair')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


### DASHBOARD


@app.route('/dashboard')
@login_required
def dashboard():
    dashboard = dashboard_viewmodel.dashboard()
    return dashboard


@app.route('/dashboard/clientes')
@login_required
def dashboard_customers():
    dashboard_customers = dashboard_viewmodel.dashboard_customers()
    return dashboard_customers   


@app.route('/dashboard/usuarios')
@login_required
def dashboard_users():
    dashboard_users = dashboard_viewmodel.dashboard_users()
    return dashboard_users   


### CLIENTES


@app.route('/cadastro-clientes', methods=['GET', 'POST'])
@login_required
def customers_registration():
    customers_registration = customers_viewmodel.customers_registration()
    return customers_registration


@app.route('/edicao-cliente/<customer_id>', methods=['POST', 'GET'])
@login_required
def customers_update(customer_id):
    customers_update = customers_viewmodel.customers_update(customer_id)
    return customers_update


### USUARIOS

# pip install flask-bcrypt
@app.route('/cadastro-usuarios', methods=['GET', 'POST'])
@login_required
def users_registration():
    user_registration = user_viewmodel.users_registration()
    return user_registration


@app.route('/edicao-usuario/<user_id>', methods=['GET', 'POST'])
@login_required
def user_update(user_id):
    user_update = user_viewmodel.user_update(user_id)
    return user_update


@app.route('/deletar-usuario/<user_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def user_delete(user_id):
   user_delete = user_viewmodel.user_delete(user_id)
   return user_delete   


@app.route('/resetar-senha/<user_id>', methods=['GET', 'POST'])
@login_required
def user_reset_password(user_id):
    users_reset_password = user_viewmodel.user_reset_password(user_id)
    return users_reset_password


@app.route('/alterar-status/<user_id>', methods=['GET', 'POST'])
def user_change_status(user_id):
    user_change_status = user_viewmodel.user_change_status(user_id)
    return user_change_status 


@app.route('/editar-senha', methods=['GET', 'POST'])
@login_required
def user_edit_password():
    #password = pegar dado da senha
    #password_crypt = bcrypt.generate_password_hash(password)
    #para usar depois de gravado no banco seria
    #bcrypt.check_password_hash(password_crypt, password)
    pass


@app.route('/empresas_sugeridas/<value>')
@login_required
def product_suggestions(value):
    search_name = value
    print(search_name)
    # products = Customers.query.order_by(Customers.name_customer).all();
    if len(search_name) >= 2:
        products = Customers.query.filter(Customers.name_customer.like(f'%{search_name}%')).all()
        suggestions = [p.name_customer for p in products]
        suggestions = sorted(suggestions) 
    else:
        suggestions = []
    print(suggestions)
    return jsonify(suggestions)


@app.route('/cadastro-ar-condicionado/', methods=["GET", "POST"], defaults={'customer_id': None})
@app.route('/cadastro-ar-condicionado/<customer_id>', methods=["GET", "POST"])
@login_required
def equipments_registration(customer_id):
    equipments_registration = equipments_viewmodel.equipments_registration(customer_id)
    return equipments_registration


@app.route('/dashboard/cliente/servicos/<customer_id>')
@login_required
def equipment_summary(customer_id):
    equipment_summary = equipments_viewmodel.equipment_summary(customer_id)
    return equipment_summary


@app.route('/dashboard/clientes/servicos/<customer_id>/filtro')
@login_required
def equipment_summary_filter(customer_id):
    equipment_summary_filter = equipments_viewmodel.equipment_summary_filter(customer_id)
    return equipment_summary_filter


@app.route('/dashboard/cliente/novo-servico/<int:customer_id>/<int:equipment_id>', methods=["POST", "GET"])
@login_required
def new_service(customer_id, equipment_id):
    new_service = services_viewmodel.new_service(customer_id, equipment_id)
    return new_service


#acesso pelo id do equipamento seguindo o fluxo do sistema
@app.route('/dashboard/cliente/relatorio-servico', defaults={'equipment_id': None})
@app.route('/dashboard/cliente/relatorio-servico/<int:equipment_id>')
@login_required
def report_service(equipment_id):
    report_service = services_viewmodel.report_service(equipment_id)
    return report_service


#acesso pelo link (qrcode)
@app.route('/dashboard/cliente/relatorio-servico/codigo', defaults={'qr_code': None})
@app.route('/dashboard/cliente/relatorio-servico/codigo/<int:qr_code>')
def report_service_qr_code(qr_code):
    equipment = None

    if qr_code is not None:
        equipment = Equipments.query.filter_by(qr_code=qr_code).first()
        customer = Customers.query.filter_by(id=equipment.id_customer).first();

    return render_template('report_service.html', equipment=equipment, customer=customer)  


#mudar nome do método e do template 
#(método algo como equipment_services)
#(template mesmo nome)
@app.route('/cliente/equipamento', defaults={"codigo": "-1"})
@app.route('/cliente/equipamento/<codigo>')
def equipmentSummary(codigo):
    equipment = ""
    if codigo == 'num_03883560235871212_qrcode':
        equipment = 'Equipamento LG num_03883560235871212_qrcode'
    if codigo == 'num_019106495463115236_qrcode':
        equipment = 'Equipamento Samsumg num_019106495463115236_qrcode' 
    return render_template('equipment_summary.html', equipment=equipment)


@app.route('/qr-code')
def qr_code():
    # print("imprimiu certo")
    # gerador_qr_codes = generate_code.createCode(list_images, 0)
    print(list_images)
    return render_template('qr_code.html', list_images=list_images)


@app.route('/generate-qrcode/<qtde>')
@login_required
def generate_qrcode(qtde):
    print("imprimiu certo")
    qtde_to_int = int(qtde)
    generate_code.createCode(list_images, qtde_to_int)
    print(list_images)
    return redirect(url_for('qr_code'))
 