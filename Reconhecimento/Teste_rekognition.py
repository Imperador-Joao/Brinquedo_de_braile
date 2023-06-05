from os import system
import boto3
import csv
from googletrans import Translator

def traduzir(texto, idioma_origem = 'en', idioma_destino = 'pt'):
    tradutor = Translator()
    traducao = tradutor.translate(texto, src = idioma_origem, dest = idioma_destino)
    return traducao.text

def tirar_foto(nome = 'foto_camera'):
    system(f"fswebcam --resolution 640x480 --skip 10 {nome}.jpg")



with open('Chaves acesso.csv','r') as credenciais:
    next(credenciais)
    chave,senha = list(csv.reader(credenciais))[0]

nome_foto = 'foto_teste'
tirar_foto(nome_foto)

resposta = input('A foto ficou boa?\t')

while resposta.lower() != 'sim':
    tirar_foto(nome_foto)
    resposta = input('A foto ficou boa?\t') 


nome_arquivo_foto = f'{nome_foto}.jpg'

cliente = boto3.client('rekognition',
                       aws_access_key_id = chave,
                       aws_secret_access_key = senha,
                       region_name = 'eu-central-1')


with open(nome_arquivo_foto,'rb') as imagem_fonte:
    bytes_fonte = imagem_fonte.read()

retorno = cliente.detect_labels(Image = {'Bytes':bytes_fonte},MaxLabels = 5)

itens_detectados = retorno.get('Labels')
imagens_confiabilidades = {traduzir(objeto.get('Name')):objeto.get('Confidence') for objeto in itens_detectados}

print(imagens_confiabilidades)