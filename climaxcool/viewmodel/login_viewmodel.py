from flask import render_template, url_for, redirect, request, flash, abort
from flask_login import login_user
from climaxcool.models import Users, Customers, Services, Equipments
from climaxcool.repository.repo_customers import Repo_Customers
from climaxcool.forms import FormSignIn
from climaxcool import database
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


repo_customers = Repo_Customers()

class Login_ViewModel():

    def login(self):
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