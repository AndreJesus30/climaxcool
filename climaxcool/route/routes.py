from climaxcool import app
from flask import render_template, url_for, redirect, request, jsonify, flash
from climaxcool.models import Users, Customers, Equipments, Services
from climaxcool.shared import generate_code
from climaxcool.forms import FormNewService, FormSignIn, FormCustomerRegistration, FormUsersRegistration, FormEquipmentsRegistration
from climaxcool import database
from flask_login import login_user, logout_user, current_user, login_required

generate_qrcodes = 'Função Gerar QR Codes'
list_qrcodes = ['qr1', 'qr2', 'qr3', 'qr4', 'qr5', 'qr6',]
list_images = []


# @app.route('/gerador-qrcodes')
# def generateQrCode():
#     # teste_list_images = url_for('static', filename=f"images/img_{1}.jpg")
#     return render_template('generate_qrcode.html', list_qrcodes=list_qrcodes, generate_qrcodes=generate_qrcodes, list_images=list_images)



@app.route('/')
def home():
    # teste_list_images = url_for('static', filename=f"images/img_{1}.jpg")
    return render_template('home.html')
  

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormSignIn()

    if form_login.validate_on_submit():
        print("formulario validado")
        user = Users.query.filter_by(username=form_login.username.data).first()
        # if user and bcrypt.check_password_hash(user.password, form_login.password.data):
        if user and user.status_user == "ATIVO" and (user.password == form_login.password.data):
            print(f"usuario logado: {user.username}")
            login_user(user, remember=True)
            flash(f'Login feito com sucesso: {form_login.username.data}', 'alert-success')

            par_next = request.args.get('next')
            #posso pegar também o request.args somente, isso trará os parametros da URL
            #neste caso estou interessado no qrcode

            if user.id_customer == 1 and par_next:
                return redirect(par_next)
            elif user.id_customer != 1 and par_next:
                #verificar se o user.id_customer pode ver o equipamento do qr code
                return "Pagina do equipamento que virá pelo QR Code"
            elif user.id_customer == 1:
                return redirect(url_for('dashboard_customers'))
            else:
                return redirect(url_for('equipment_summary', customer_id=user.id_customer))

        else:
            flash(f'Falha no login. Usuario ou Senha incorretos.', 'alert-danger')

    return render_template('login.html', form_login=form_login)


@app.route('/sair')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard():
    customers = [];
    return render_template('dashboard.html', customers=customers, type_data='')


@app.route('/dashboard/clientes')
@login_required
def dashboard_customers():
    name = request.args.get('name_customer_input');
    print(name);

    if name:
        customers = Customers.query.filter(Customers.name_customer.ilike(f'%{name}%')).all();
    elif name != None:
        customers = Customers.query.order_by(Customers.name_customer).all();
    else:
        customers = [];     

    return render_template('dashboard.html', customers=customers, type_data='clientes')    


@app.route('/dashboard/usuarios')
@login_required
def dashboard_users():
    name = request.args.get('name_customer_input');
    print(name);

    if name:
        customers = Users.query.filter(Users.username.ilike(f'%{name}%')).all();
    elif name != None:
        customers = Users.query.order_by(Users.username).all();
    else:
        customers = [];     

    return render_template('dashboard.html', customers=customers, type_data='usuarios')    


@app.route('/cadastro-clientes', methods=['GET', 'POST'])
@login_required
def customers_registration():
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
            id_user= 1
        )
        database.session.add(new_customer)
        database.session.commit()
        print('salvo no banco de dados')
        flash('Cliente cadastrado com sucesso', 'alert-success'),
        return redirect(url_for('dashboard_customers'))
    return render_template('customer_registration.html', form_customer=form_customer)


# pip install flask-bcrypt
@app.route('/cadastro-usuarios', methods=['GET', 'POST'])
@login_required
def users_registration():
    form_users = FormUsersRegistration()
    customers = Customers.query.order_by(Customers.name_customer).all();

    if form_users.validate_on_submit():
        print('formulário validado')
        selected_customer = request.form.get('selected_customer')
        print(f'cliente selecionado {selected_customer}')
        customer = Customers.query.filter_by(name_customer=selected_customer).first();
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

    return render_template('users_registration.html', form_users=form_users, customers=customers)


@app.route('/editar-usuarios', methods=['GET', 'POST'])
@login_required
def users_edit():
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
                id_user=1,
            )
            database.session.add(new_equipments)
            database.session.commit()
            flash('Equipamento cadastrado com sucesso', 'alert-success')
            return redirect(url_for('dashboard'))

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
                id_user=1,
            )
            database.session.add(new_equipments)
            database.session.commit()
            return redirect(url_for('equipment_summary', customer_id=customer_id))

       
    return render_template('equipments_registration.html', form_equipments=form_equipments)     


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


@app.route('/dashboard/cliente/servicos/<customer_id>')
@login_required
def equipment_summary(customer_id):
    customer = Customers.query.filter_by(id=customer_id).first();
    equipments = Equipments.query.filter_by(id_customer=customer_id).all();

    print(equipments);

    return render_template('summary_equipments.html', customer=customer, equipments=equipments)


@app.route('/dashboard/clientes/servicos/<customer_id>/filtro')
@login_required
def equipment_summary_filter(customer_id):
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



@app.route('/dashboard/cliente/novo-servico/<int:customer_id>/<int:equipment_id>', methods=["POST", "GET"])
@login_required
def new_service(customer_id, equipment_id):
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


class report_service_model:
    def __init__(self, id, date, list_services, annotations, expert, price):
        self.id = id
        self.date = date
        self.list_services = list_services
        self.annotations = annotations
        self.expert = expert
        self.price = price


#acesso pelo id do equipamento seguido o fluxo do sistema
@app.route('/dashboard/cliente/relatorio-servico', defaults={'equipment_id': None})
@app.route('/dashboard/cliente/relatorio-servico/<int:equipment_id>')
@login_required
def report_service(equipment_id):
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
 