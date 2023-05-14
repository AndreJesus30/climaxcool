from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateTimeField, SelectField, TextAreaField,  IntegerField, RadioField, BooleanField
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


class FormEquipmentsRegistration(FlaskForm):
    name_equipment = TextAreaField('Nome', validators=[DataRequired()])
    brand_equipment = StringField('Marca', validators=[DataRequired()])
    address = TextAreaField('Local', validators=[DataRequired()])
    qr_code = StringField('QR-Code')
    status_equipment = StringField('Status',default="Ativo")
    customer = SelectField('Cliente', validators=[DataRequired()], choices=[' ','Empresa 1', 'Empresa 2', "Empresa 3", "João"]) 
    btn_submit_equip_registration = SubmitField('Cadastrar Equipamento')


class FormNewService(FlaskForm):
    service_installation = BooleanField('Instalação')
    service_disassembly = BooleanField('Desmontagem')
    service_preventive_maintenance = BooleanField('Manutenção Preventiva')
    service_corrective_maintenance = BooleanField('Manutenção Corretiva')
    service_chemical_maintenance = BooleanField('Manutenção Química')
    service_filter_cleaning = BooleanField('Limpeza de Filtros')
    service_drain_clearing = BooleanField('Desobstrução de Dreno')
    service_gas_charging = BooleanField('Carga de Gás')
    service_electronic_board_repair = BooleanField('Reparo na Placa Eletrônica')
    service_capacitor_replacement = BooleanField('Troca de Capacitor')
    service_internal_fan_mode_exchange = BooleanField('Troca do Modo Ventilador Interno')
    service_external_fan_mode_exchange = BooleanField('Troca do Modo Ventilador Externo')
    service_compressor_replacement = BooleanField('Troca do Compressor')
    annotations = TextAreaField('Observações')
    expert = SelectField('Técnico', validators=[DataRequired()], choices=[' ','João', 'Carlos', "Cleber", "Marcos"]) 
    price = FloatField('Preço')
    btn_submit_new_service = SubmitField("Salvar")
