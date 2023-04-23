from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateTimeField, SelectField, TextAreaField,  IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange


# class FormSignUp(FlaskForm):
#     username = StringField('Nome Completo', validators=[DataRequired(), Length(2, 50)])
#     email = StringField('E-mail', validators=[DataRequired(), Email()])
#     password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
#     password_check = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('password')])
#     btn_submit_signUp = SubmitField('Criar Conta')


class FormSignIn(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    btn_submit_signIn = SubmitField('Fazer Login')


class FormCustomerRegistration(FlaskForm):
    type_customer = RadioField('Tipo de Cliente', choices=["Pessoa Jurídica", "Pessoa Física"], validators=[DataRequired()]) 
    number_register_customer =  StringField('CNPJ')
    name_customer = StringField('Nome Fantasia', validators=[DataRequired()])
    name_responsible = StringField('Nome do Responsável')
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    address = TextAreaField('Endereço')
    telephone_fixed = StringField('Telefone Fixo')
    telephone_mobile = StringField('Celular')
    reference_point = TextAreaField('Ponto de Referencia')
    btn_submit_customer = SubmitField('Cadastrar Cliente')


class FormUsersRegistration(FlaskForm):
    type_user = RadioField('Tipo de Usuário', choices=["Funcionário", "Externo"],  validators=[DataRequired()]) 
    username = StringField('Nome Completo', validators=[DataRequired(), Length(3, 50)])
    email = StringField('E-mail', validators=[Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    password_check = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('password')])
    permission_user = StringField('Permissão', validators=[DataRequired()]) 
    #status_user = StringField('Status Usuário', validators=[DataRequired()])
    #fazer vinculo do texto com o numero da permissão 0, 1, 2..
    #company = StringField('Empresa', validators=[DataRequired()])
    btn_submit_user_registration = SubmitField('Cadastrar Usuário')