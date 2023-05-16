from climaxcool import app
from flask import render_template, url_for, redirect, request, jsonify, flash
from climaxcool.models import Users, Customers, Equipments, Services, ListForServices
from climaxcool.shared import generate_code
from climaxcool.forms import FormNewService, FormSignIn, FormCustomerRegistration, FormUsersRegistration, FormEquipmentsRegistration
from climaxcool import database

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
    # form_criarconta = FormCriarConta()

    # if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
    #     usuario = Usuario.query.filter_by(email=form_login.email.data).first()
    #     if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
    #         login_user(usuario, remember=form_login.lembrar_dados.data)
    #         flash(f'login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
    #         par_next = request.args.get('next')
    #         if par_next:
    #             return redirect(par_next)
    #         else:
    #             return redirect(url_for('home'))
    #     else:
    #         flash(f'Falha no login. E-mail ou Senha Incorretos', 'alert-danger')

    # if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
    #     senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
    #     usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
    #     database.session.add(usuario)
    #     database.session.commit()
    #     login_user(usuario)
    #     flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
    #     return redirect(url_for('home'))

    # return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)
    return render_template('login.html', form_login=form_login)


@app.route('/dashboard')
def dashboard():
    customers = [];
    return render_template('dashboard.html', customers=customers, type_data='')


# @app.route('/dashboard/clientes')
# def dashboard_customers():
#     customers = Customer.query.order_by(Customer.name_customer).all();
#     return render_template('dashboard.html', customers=customers)


# @app.route('/dashboard/cliente/<name>')
# def dashboard_customer(name):
#     # customer = Customer.query.filter_by(id=customer_id)
#     customer = Customer.query.filter(Customer.name_customer.ilike(f'%{name}%')).all()
#     return render_template('dashboard.html', customers=customer)    


@app.route('/dashboard/clientes')
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
        #flash('Cliente cadastrado com sucesso', 'alert-success'),
        return redirect(url_for('dashboard_customers'))
    return render_template('customer_registration.html', form_customer=form_customer)


@app.route('/cadastro-usuarios', methods=['GET', 'POST'])
def users_registration():
    form_users = FormUsersRegistration()
    print("fora da validação")

    company_field = request.args.get('company_user') 
    print(company_field)
    customers = Customers.query.order_by(Customers.name_customer).all();

    if form_users.validate_on_submit():
        print('formulário validado')
        new_user = Users(
            type_user=form_users.type_user.data,
            username=form_users.username.data, 
            email=form_users.email.data,
            password=form_users.password.data,
            #permission_user=form_users.permission_user.data
        )
        database.session.add(new_user)
        database.session.commit()
        print('salvo no banco de dados')
        return redirect(url_for('dashboard_users'))

    return render_template('users_registration.html', form_users=form_users, customers=customers)


@app.route('/empresas_sugeridas/<value>')
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
                name_equipment=form_equipments.name_equipment.data,
                brand_equipment=form_equipments.brand_equipment.data, 
                address=form_equipments.address.data,
                qr_code= None if not form_equipments.qr_code.data else form_equipments.qr_code.data,
                id_customer= id_customer,
                id_user=1,
            )
            database.session.add(new_equipments)
            database.session.commit()
            return redirect(url_for('dashboard'))

    if customer_id:
        form_equipments = FormEquipmentsRegistration()
        customer = Customers.query.filter_by(id=customer_id).first();
        form_equipments.customer.choices = [customer.name_customer];
        form_equipments.customer.data = customer.name_customer;

        if form_equipments.validate_on_submit():
            
            new_equipments = Equipments(
                name_equipment=form_equipments.name_equipment.data,
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
def generate_qrcode(qtde):
    print("imprimiu certo")
    qtde_to_int = int(qtde)
    generate_code.createCode(list_images, qtde_to_int)
    print(list_images)
    return redirect(url_for('qr_code'))


@app.route('/dashboard/cliente/servicos/<customer_id>')
def equipment_summary(customer_id):
    customer = Customers.query.filter_by(id=customer_id).first();
    equipments = Equipments.query.filter_by(id_customer=customer_id).all();

    print(equipments);

    return render_template('summary_equipments.html', customer=customer, equipments=equipments)


@app.route('/dashboard/clientes/servicos/<customer_id>/filtro')
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
def new_service(customer_id, equipment_id):
    form_new_service = FormNewService()

    customer = Customers.query.filter_by(id=customer_id).first()
    equipment = Equipments.query.filter_by(id=equipment_id).first()

    #if permissão total pode escolher qualquer técnico
    #senão só tem a opção de escolher ele mesmo como técnico
    #criar essas condições após terminar authenticação e estrutura de permissões

    if form_new_service.validate_on_submit:
        new_service = Services(
            annotations = form_new_service.annotations.data,
            price = form_new_service.price.data,
            id_customer = customer_id,
            id_equipment = equipment_id,
            id_expert = 1
        )
        database.session.add(new_service)
        database.session.commit()

        new_service_id = new_service.id
        print(new_service_id)

        if new_service_id is not None:
            for service in form_new_service:
                if "service_" in service.name and service.data:
                    print(f"{service.data}  {service.name}  {service.label.text}")
                    new_list_for_services = ListForServices(
                        service = service.label.text,
                        id_service = new_service_id,
                        id_customer = customer_id,
                        id_equipment = equipment_id,   
                    )
                    database.session.add(new_list_for_services)
                    database.session.commit()

    return render_template('new_service.html', form_new_service=form_new_service, customer=customer, equipment=equipment)



#acesso pelo id do equipamento seguido o fluxo do sistema
@app.route('/dashboard/cliente/relatorio-servico', defaults={'equipment_id': None})
@app.route('/dashboard/cliente/relatorio-servico/<int:equipment_id>')
def report_service(equipment_id):
    equipment = None

    if equipment_id is not None:
        equipment = Equipments.query.filter_by(id=equipment_id).first()
        customer = Customers.query.filter_by(id=equipment.id_customer).first();

    return render_template('report_service.html', equipment=equipment, customer=customer)  


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
 