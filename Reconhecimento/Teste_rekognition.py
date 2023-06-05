from os import system
import boto3
import csv



def tirar_foto(nome = 'foto_camera'):
    system(f"fswebcam --resolution 640x480 --skip 10 {nome}.jpg")



with open('Chaves acesso.csv','r') as credenciais:
    next(credenciais)
    chave,senha = list(csv.reader(credenciais))[0]

nome_foto = 'eu'
#tirar_foto(nome_foto)

nome_arquivo_foto = f'{nome_foto}.jpg'

cliente = boto3.client('rekognition',
                       aws_access_key_id = chave,
                       aws_secret_access_key = senha,
                       region_name = 'eu-central-1')


with open(nome_arquivo_foto,'rb') as imagem_fonte:
    bytes_fonte = imagem_fonte.read()

resposta = cliente.detect_labels(Image = {'Bytes':bytes_fonte},MaxLabels = 10)

for chave,valor in resposta.items():
    print(f'{chave}\t {valor}\n')
