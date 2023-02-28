from climaxcool import app
from flask import Flask, render_template, url_for, redirect
from climaxcool.shared import generate_code
from climaxcool.forms import FormSignIn, FormSignUp, FormCustomerRegistration, FormUsersRegistration

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
    return render_template('dashboard.html')


@app.route('/cadastro-clientes')
def customers_registration():
    form_customer = FormCustomerRegistration()
    return render_template('customer_registration.html', form_customer=form_customer)


@app.route('/cadastro-usuarios')
def users_registration():
    form_users = FormUsersRegistration()
    return render_template('users_registration.html', form_users=form_users)


@app.route('/imprimir')
def imprimir():
    print("imprimiu certo")
    generate_code.createCode(list_images)
    print(list_images)
    return redirect(url_for('generateQrCode'))


@app.route('/dashboard/cliente/novo_serviço')
def newService():
    return render_template('new_service.html')


@app.route('/dashboard/cliente/relatorio-serviço')
def report_service():
    return render_template('report_service.html')  


@app.route('/cliente/equipamento', defaults={"codigo": "-1"})
@app.route('/cliente/equipamento/<codigo>')
def equipmentSummary(codigo):
    equipment = ""
    if codigo == 'num_03883560235871212_qrcode':
        equipment = 'Equipamento LG num_03883560235871212_qrcode'
    if codigo == 'num_019106495463115236_qrcode':
        equipment = 'Equipamento Samsumg num_019106495463115236_qrcode' 
    return render_template('equipment_summary.html', equipment=equipment)
 