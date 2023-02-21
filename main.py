from flask import Flask, render_template, url_for, redirect
from shared import generate_code

app = Flask(__name__)

generate_qrcodes = 'Função Gerar QR Codes'
list_qrcodes = ['qr1', 'qr2', 'qr3', 'qr4', 'qr5', 'qr6',]
list_images = []


# @app.route('/')
# def generateQrCode():
#     # teste_list_images = url_for('static', filename=f"images/img_{1}.jpg")
#     return render_template('generate_qrcode.html', list_qrcodes=list_qrcodes, generate_qrcodes=generate_qrcodes, list_images=list_images)



@app.route('/')
def homePage():
    # teste_list_images = url_for('static', filename=f"images/img_{1}.jpg")
    return render_template('home_page.html')


@app.route('/novo_serviço')
def newService():
    return render_template('new_service.html')    


@app.route('/imprimir')
def imprimir():
    print("imprimiu certo")
    generate_code.createCode(list_images)
    print(list_images)
    return redirect(url_for('generateQrCode'))


@app.route('/cliente/equipamento', defaults={"codigo": "-1"})
@app.route('/cliente/equipamento/<codigo>')
def equipmentSummary(codigo):
    equipment = ""
    if codigo == 'num_03883560235871212_qrcode':
        equipment = 'Equipamento LG num_03883560235871212_qrcode'
    if codigo == 'num_019106495463115236_qrcode':
        equipment = 'Equipamento Samsumg num_019106495463115236_qrcode' 
    return render_template('equipment_summary.html', equipment=equipment)




if __name__ == '__main__':
    app.run(debug=True)    