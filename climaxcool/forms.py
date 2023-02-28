from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateTimeField, SelectField, TextAreaField,  IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange


class FormSignUp(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    password_check = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('password')])
    btn_submit_signUp = SubmitField('Criar Conta')


class FormSignIn(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    btn_submit_signIn = SubmitField('Fazer Login')


class FormCustomerRegistration(FlaskForm):
    type_customer = RadioField('Tipo de Cliente', choices=["Pessoa Jurídica", "Pessoa Física"]) 
    number_cnpj =  IntegerField('CNPJ')
    number_cpf = IntegerField('CPF')
    name_company = StringField('Nome Empresa')
    name_customer = StringField('Nome')
    email = StringField('E-mail', validators=[Email()])
    address = TextAreaField('Endereço')
    referencePoint = TextAreaField('Ponto de Referencia')
    btn_submit_customer = SubmitField('Cadastrar Cliente')


class FormUsersRegistration(FlaskForm):
    type_user = RadioField('Tipo de Usuário', choices=["Funcionário", "Externo"]) 
    number_rg = IntegerField('RG')
    name_user = StringField('Nome Completo')
    email = StringField('E-mail', validators=[Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    btn_submit_user_registration = SubmitField('Cadastrar Usuário')