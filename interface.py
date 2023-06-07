#Bibliotecas
import tkinter as tk
from PIL import ImageTk, Image
from serial import Serial
from os import system
import csv
from requests import get, post
from datetime import datetime, timedelta
from utilitarios.dicionario import traduzir
from reconhecimento.detector import tirar_foto,Detector_aws

#Variáveis globais
global imagem, path, data_foto
global painel_foto, etiqueta_foto
global palavra_traduzida
global meu_serial

data_foto = ''

#Inicia serial
#meu_serial = Serial("COM26", baudrate = 9600, timeout = 0.1)


#Chave amozon
with open('reconhecimento/Chave aws.csv','r') as credenciais:
    next(credenciais)
    chave,senha = list(csv.reader(credenciais))[0]

#Criação da janela
janela = tk.Tk()
janela.title("Interface")
janela.geometry("550x500")

#Janela foto
painel_foto = tk.Label(janela, background = "grey", width = 57, height = 17)
painel_foto.place(x = 12, y = 17)
etiqueta_foto = tk.Label(janela, text = "Tire uma foto", fg = "white" , bg = "grey", font = ('arial', 15, 'bold'))
etiqueta_foto.place(x = 150, y = 135)

#Janela palavra
janela_botoes = tk.Canvas(janela, background = "black", width = 123, height = 160)
janela_botoes.place(x = 420, y = 116)
janela_botoes2 = tk.Canvas(janela, background = "grey93", width = 113, height = 150)
janela_botoes2.place(x = 425, y = 121)

#Botões
    #Janela

largura_externa_janela_botoes, largura_interna_janela_botoes= 123,111
altura_externa_janela_botoes,altura_interna_janela_botoes = 95,85

janela_botoes = tk.Canvas(janela, background = "black", width = largura_externa_janela_botoes,
                           height = altura_externa_janela_botoes)
janela_botoes.place(x = 420, y = 15)
janela_botoes2 = tk.Canvas(janela, background = "grey93", width = largura_interna_janela_botoes,
                            height = altura_interna_janela_botoes)
janela_botoes2.place(x = 425, y = 20)

    #Fotografar
def fotografar():
    global imagem, path,data_foto
    
        #captura imagem
    data_foto = datetime.now().strftime('Foto_teste_%d_%m_%y__%H:%M:%S')
    

    '''
    #envia comando para o sistema
#     comando_win = "CommandCam /filename " + data_foto + ".jpg /delay 500"
    comando_lin = "fswebcam --resolution 640x480 --skip 10 " + data_foto + ".jpg"
#     system(comando_win)
    system(comando_lin)
    '''

    sistema_operacional = 'Linux'

    tirar_foto(nome = data_foto,sistema_operacional = sistema_operacional)
    
    print("Tirei foto!")
    
    path = f'{data_foto}.jpg'
#     path = "foto_telegram.jpg"
    
        #abrir imagem
    imagem = Image.open(path)
    
        #redimenciona
    redimencionada = imagem.resize((400, 257), Image.LANCZOS)
        
        #projeta
    nova_imagem = ImageTk.PhotoImage(redimencionada)
    painel_foto.config(image = nova_imagem, width = 400, height = 257)
    painel_foto.image = nova_imagem
    
        #destroi Label de texto
    etiqueta_foto.destroy()

        #ativa botão de upload
    botao_upload['state'] = tk.NORMAL







    #Upload
def envia_foto():
    global etiqueta_foto, palavra_traduzida, meu_serial
    print("Enviando para a IA")
    
    
    detector_amazon = Detector_aws(senha = senha,chave = chave)
    nome_arquivo_foto = f'{data_foto}.jpg'
    with open(nome_arquivo_foto,'rb') as imagem_fonte:
        bytes_fonte = imagem_fonte.read()
    
    itens_detectados = detector_amazon.receber_dados(bytes_imagem = bytes_fonte,etiquetas = 8).get('Labels')

    
    palavra_maior_confianca = itens_detectados[0].get('Name')
    palavra_traduzida = traduzir(texto=palavra_maior_confianca)


    etiqueta_palavra = tk.Label(janela,text = palavra_traduzida,bg = 'grey93')
    etiqueta_palavra.place(x = 450,y = 130)

    
        #envia palavra pro arduino
    #palavra_traduzida += '\n'
    #meu_serial.write(palavra_traduzida.encode("UTF-8"))

        #muda janela foto para o padão
    imagem_grey = tk.PhotoImage('cinza.jpg')
    painel_foto.config(image = imagem_grey, width = 400, height = 257)
    painel_foto.image = imagem_grey
    etiqueta_foto = tk.Label(janela, text = "Tire uma foto", fg = "white" , bg = "grey")
    etiqueta_foto.place(x = 176, y = 135)
    
        #desativa botão de upload
    botao_upload['state'] = tk.DISABLED


botao_fotografar = tk.Button(janela, text = "Fotografar",font = ('arial',8), command = fotografar)
botao_fotografar.place(x = 450, y = 35)

botao_upload = tk.Button(janela, text = "Upload", command = envia_foto, state = 'disabled')
botao_upload.place(x = 457, y = 65)

#Braile
    #Etiqueta
etiqueta_braile = tk.Label(janela, text = "Braile")
etiqueta_braile.place(x = 15, y = 280)

    #Janela
janela_braile = tk.Canvas(janela, background = "white", width = 525, height = 185)
janela_braile.place(x = 10, y = 300)

    #Função auxiliar
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

    #Importa braile //apenas palavras com 4 letras
# braile = meu_serial.readline().decode().strip()
braile = "101110, 111110, 110101, 101101"

    #Trata braile //101}coluna 1, 110}coluna 2
if braile:
        #separa os digitos e transfoma para inteiro
    dig1 = int(braile[0:6])
    dig2 = int(braile[8:14])
    dig3 = int(braile[16:-8])
    dig4 = int(braile[-6:])
        
        #dicionário de digitos de dicionário de colunas de dicionário de bolas //cada bola diz seu estado 0 abaixada, 1 levantada
    dicionario_braile = [('dig1',
                          [('col1',
                              [('bol1', int(dig1/100000)),
                               ('bol2', int((dig1/10000))%10),
                               ('bol3', int((dig1/1000))%10)]),
                            ('col2',
                             [('bol1', int((dig1/100))%10),
                              ('bol2', int((dig1/10))%10),
                              ('bol3', int(dig1%10))])]),
                          
                          ('dig2',
                           [('col1',
                             [('bol1', int(dig2/100000)),
                              ('bol2', int((dig2/10000))%10),
                              ('bol3', int((dig2/1000))%10)]),
                            ('col2',
                             [('bol1', int((dig2/100))%10),
                              ('bol2', int((dig2/10))%10),
                              ('bol3', int(dig2%10))])]),
                          
                          ('dig3',
                           [('col1',
                             [('bol1', int(dig3/100000)),
                              ('bol2', int((dig3/10000))%10),
                              ('bol3', int((dig3/1000))%10)]),
                            ('col2',
                             [('bol1', int((dig3/100))%10),
                              ('bol2', int((dig3/10))%10),
                              ('bol3', int(dig3%10))])]),
                          
                          ('dig4',
                           [('col1',
                             [('bol1', int(dig4/100000)),
                              ('bol2', int((dig4/10000))%10),
                              ('bol3', int((dig4/1000))%10)]),
                            ('col2',
                             [('bol1', int((dig4/100))%10),
                              ('bol2', int((dig4/10))%10),
                              ('bol3', int(dig4%10))])])]
    

    #Desenho //fill = white -> 0/false, fill = black -> 1/true
        #digito 1
            #coluna 1
janela_braile.create_circle(60, 45, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(60, 95, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(60, 145, 10, fill="white", outline="grey", width=2)

            #coluna 2
janela_braile.create_circle(110, 45, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(110, 95, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(110, 145, 10, fill="white", outline="grey", width=2)

        #digito 2
            #coluna 1
janela_braile.create_circle(180, 45, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(180, 95, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(180, 145, 10, fill="white", outline="grey", width=2)

            #coluna 2
janela_braile.create_circle(230, 45, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(230, 95, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(230, 145, 10, fill="white", outline="grey", width=2)

        #digito 3
            #coluna 1
janela_braile.create_circle(300, 45, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(300, 95, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(300, 145, 10, fill="white", outline="grey", width=2)

            #coluna 2
janela_braile.create_circle(350, 45, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(350, 95, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(350, 145, 10, fill="white", outline="grey", width=2)

        #digito 4
            #coluna 1
janela_braile.create_circle(420, 45, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(420, 95, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(420, 145, 10, fill="white", outline="grey", width=2)

            #coluna 2
janela_braile.create_circle(470, 45, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(470, 95, 10, fill="white", outline="grey", width=2)
janela_braile.create_circle(470, 145, 10, fill="white", outline="grey", width=2)

    #Exibe braile






janela.tk.mainloop()
