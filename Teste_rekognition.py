
from utilitarios.dicionario import traduzir
from reconhecimento.detector import Detector,tirar_foto
import csv


with open('reconhecimento/Chaves acesso.csv','r') as credenciais:
    next(credenciais)
    chave,senha = list(csv.reader(credenciais))[0]

nome_foto = 'foto_teste'
tirar_foto(nome_foto)
nome_arquivo_foto = f'{nome_foto}.jpg'

meu_detector = Detector(senha = senha,chave = chave)



with open(nome_arquivo_foto,'rb') as imagem_fonte:
    bytes_fonte = imagem_fonte.read()




itens_detectados = meu_detector.receber_dados(bytes_imagem = bytes_fonte).get('Labels')
imagens_confiabilidades = {traduzir(objeto.get('Name')):objeto.get('Confidence') for objeto in itens_detectados}

print(imagens_confiabilidades)