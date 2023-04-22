from climaxcool import app
from flask import render_template, url_for, redirect, request, flash
from climaxcool.models import User, Customer
from climaxcool.shared import generate_code
from climaxcool.forms import FormSignIn, FormCustomerRegistration, FormUsersRegistration
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
    users = User.query.all();
    customers = [];
    return render_template('dashboard.html', customers=customers)


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
        customers = Customer.query.filter(Customer.name_customer.ilike(f'%{name}%')).all();
    else:
        customers = Customer.query.order_by(Customer.name_customer).all();

    return render_template('dashboard.html', customers=customers)    






@app.route('/cadastro-clientes', methods=['GET', 'POST'])
def customers_registration():
    form_customer = FormCustomerRegistration()

    if form_customer.validate_on_submit():
        print('formulário validado')
        new_customer = Customer(
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
        return redirect(url_for('dashboard'))
    return render_template('customer_registration.html', form_customer=form_customer)


@app.route('/cadastro-usuarios', methods=['GET', 'POST'])
def users_registration():
    form_users = FormUsersRegistration()
    print("fora da validação")

    if form_users.validate_on_submit():
        print('formulário validado')
        new_user = User(
            type_user=form_users.type_user.data,
            username=form_users.username.data, 
            email=form_users.email.data,
            password=form_users.password.data
        )
        database.session.add(new_user)
        database.session.commit()
        print('salvo no banco de dados')
        return redirect(url_for('dashboard'))

    return render_template('users_registration.html', form_users=form_users)


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
    customer_name = "";
    if customer_id == "1":
        customer_name = "Papelaria Tributária";
    return render_template('summary_equipments.html',  customer_name=customer_name)


@app.route('/dashboard/cliente/novo-servico')
def new_service():
    return render_template('new_service.html')


@app.route('/dashboard/cliente/relatorio-servico')
def report_service():
    return render_template('report_service.html')  



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
 