import qrcode
import random as r
import os, glob


def numRandom():    
    num_random = r.random()
    num_convert = str(num_random)

    sem_virgula = num_convert.split('.')
    num_final = f"{sem_virgula[0]}{sem_virgula[1]}"
    #print(num_final)
    return num_final


def createCode(list):
    if len(list) > 0:
        list.clear()

    dir = 'static/qrcodes'
    
    for file in os.scandir(dir):
        print(f"QR Codes excluídos: {file.path}")
        os.remove(file.path)

    for i in range(2):
        num_random = numRandom()
        IMAGEM = qrcode.make(f"site/{num_random}")
        IMAGEM.save(f"static/qrcodes/num_{num_random}_qrcode.jpg")
        item_list = f"num_{num_random}_qrcode.jpg"
        list.append(item_list)

#createCode()        