from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateTimeField, SelectField, TextAreaField, HiddenField, RadioField, BooleanField 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, NumberRange
from climaxcool.models import Users, Customers



class FormSignIn(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    btn_submit_signIn = SubmitField('Fazer Login')


user = Users()

class FormChangePassword(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha atual', validators=[DataRequired(), Length(6, 20)])
    new_password = PasswordField('Nova Senha', validators=[DataRequired(), Length(6, 20)])
    new_password_confirmed = PasswordField('Confirmar Senha', validators=[DataRequired() , Length(6, 20), EqualTo('new_password')])
    btn_submit_signIn = SubmitField('Alterar Senha')


    def validate_username(self, username):
        global user
        user = Users.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('Usuário não existe em nosso banco de dados.')
        
        pass

    def validate_password(self, password):
        global user

        if user:
            if user.password != password.data:
                raise ValidationError('A senha digitada está errada.')

        pass

         


class FormCustomerRegistration(FlaskForm):
    edit_mode = HiddenField()
    type_customer = RadioField('Tipo de Cliente', choices=["Pessoa Jurídica", "Pessoa Física"], validators=[DataRequired()]) 
    number_register_customer =  StringField('CNPJ')
    name_customer = StringField('Nome Fantasia', validators=[DataRequired()])
    name_responsible = StringField('Nome do Responsável')
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    address = TextAreaField('Endereço')
    telephone_fixed = StringField('Telefone Fixo')
    telephone_mobile = StringField('Celular')
    reference_point = TextAreaField('Ponto de Referencia')
    status_customer = SelectField('Status',validators=[Optional()], choices=['ATIVO', 'INATIVO']) 
    btn_submit_customer = SubmitField('Cadastrar Cliente')

    def validate_number_register_customer(self, number_register_customer):
        if self.edit_mode.data == 'True':
            return  # Ignora a validação durante a edição
        
        customer = Customers.query.filter_by(number_register_customer=number_register_customer.data).first()
        if customer:
            raise ValidationError('Já existe um cliente cadastrado com esse numero.')
        pass

    def validate_email(self, email):
        if self.edit_mode.data == 'True':
            return  # Ignora a validação durante a edição
        
        customer = Customers.query.filter_by(email=email.data).first()
        if customer:
            raise ValidationError('Esse e-mail já foi cadastrado em outro cliente')
        pass


class FormUsersRegistration(FlaskForm):
    edit_mode = HiddenField()
    type_user = RadioField('Tipo de Usuário', choices=["Funcionário", "Externo"],  validators=[DataRequired()]) 
    username = StringField('Nome Completo', validators=[DataRequired(), Length(3, 50)])
    email = StringField('E-mail', validators=[Optional(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    password_check = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('password')])
    permission_user = StringField('Permissão', validators=[DataRequired()]) 
    status_user = SelectField('Status', validators=[Optional()], choices=['ATIVO', 'INATIVO']) 
    btn_submit_user_registration = SubmitField('Cadastrar Usuário')

    def validate_username(self, username):
        if self.edit_mode.data == 'True':
            return  # Ignora a validação durante a edição
        
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Já existe um usuário com esse nome cadastrado')
        pass

    def validate_email(self, email):
        if self.edit_mode.data == 'True':
            return  # Ignora a validação durante a edição
        
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Esse e-mail já foi cadastrado em outro usuário')
        pass    

list_brands = ["","Agratto","Britânia","Car Bluetooth","Comfee","Consul","Daikin","Elgin","Equation","Fontaine","Fujitsu","Philco","LG","Samsung","Carrier","Fujitsu","Gree","Electrolux","Springer Midea","TCL", "Outra"]
list_btus = [7000,7500,9000,12000,15000,16000,18000,20000,24000,28000,30000,32000,36000,40000,42000,48000,58000,60000]

class FormEquipmentsRegistration(FlaskForm):
    edit_mode = HiddenField()
    brand_equipment = SelectField('Marca', validators=[DataRequired()], choices=list_brands)
    btus_equipment = SelectField('BTUs', validators=[DataRequired()], choices=list_btus) 
    address = TextAreaField('Local', validators=[DataRequired()])
    qr_code = StringField('QR-Code')
    status_equipment = SelectField('Status', validators=[Optional()], choices=['ATIVO', 'INATIVO'])
    customer = SelectField('Cliente', validators=[DataRequired()], choices=[' ']) 
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
