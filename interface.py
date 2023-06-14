#Bibliotecas
import tkinter as tk
from PIL import ImageTk, Image
from serial import Serial
import cv2 as cv
from requests import get, post
from datetime import datetime, timedelta
# from utilitarios.dicionario import traduzir, escrever_braile
# from reconhecimento.detector import tirar_foto, Detector_aws

#Variáveis globais
global imagem, nome_arquivo_foto
global painel_foto
global braile
global meu_serial

# braile = []

#Inicia serial
#meu_serial = Serial("COM26", baudrate = 9600, timeout = 0.1)

#Inicia vídeo
stream = cv.VideoCapture(0)
if (stream.isOpened() == False):
  print("Câmera não encontrada")

#Chave amozon
# with open('reconhecimento/Chave aws.csv','r') as credenciais:
#     next(credenciais)
#     chave,senha = list(csv.reader(credenciais))[0]

#Criação da janela
janela = tk.Tk()
janela.title("Interface")
janela.geometry("557x376")

#Janela foto
painel_foto = tk.Label(janela, background = "grey", width = 57, height = 17)
painel_foto.place(x = 12, y = 17)

#Janela palavra
janela_botoes = tk.Canvas(janela, background = "black", width = 123, height = 160)
janela_botoes.place(x = 420, y = 116)
janela_botoes2 = tk.Canvas(janela, background = "grey93", width = 113, height = 150)
janela_botoes2.place(x = 425, y = 121)

#Botões
    #Janela

janela_botoes_interno = tk.Canvas(janela, background = "black", width = 123, height = 95)
janela_botoes_interno.place(x = 420, y = 15)
janela_botoes_externo = tk.Canvas(janela, background = "grey93", width = 113, height = 85)
janela_botoes_externo.place(x = 425, y = 20)

    #Fotografar
def fotografar():
    global imagem, nome_arquivo_foto
    
        #tira foto
    imagem = Image.fromarray(video_tratado) 
    nome_arquivo_foto = datetime.now().strftime('Foto_teste_%d_%m_%y__%H_%M_%S.jpg')    
    imagem.save(nome_arquivo_foto)

#     tirar_foto(nome = data_foto,sistema_operacional = sistema_operacional)
    
    print("Tirei foto!")

        #ativa botão de upload
    botao_upload['state'] = tk.NORMAL

    #Upload
def envia_foto():
    global meu_serial, nome_arquivo_foto, braile
    print("Enviando para a IA")
    
        #enviar foto para o identificador da amazon
#     detector_amazon = Detector_aws(senha = senha, chave = chave)
#     with open(nome_arquivo_foto,'rb') as imagem_fonte:
#         bytes_fonte = imagem_fonte.read()
#     
        #recebe itens detectados
#     itens_detectados = detector_amazon.receber_dados(bytes_imagem = bytes_fonte, etiquetas = 8).get('Labels')

        #separa palavra com maior confiança
#     palavra_maior_confianca = itens_detectados[0].get('Name')
    
        #traduz palavra
            #en -> pt-br
#     palavra_traduzida = traduzir(texto=palavra_maior_confianca)
    
            #pt-br -> braile
#     braile = escrever_braile(palavra_traduzida)

        #exibe palavra traduzida
#     etiqueta_palavra = tk.Label(janela, text = palavra_traduzida, bg = 'grey93')
#     etiqueta_palavra.place(x = 450,y = 130)
    
        #envia palavra traduzida e braile pro arduino
#     palavra_traduzida += '\n'
#     braile_arduino = braile = '\n'
#     meu_serial.write(palavra_traduzida.encode("UTF-8"))
#     meu_serial.write(braile_arduino.encode("UTF-8"))

        #desativa botão de upload
    botao_upload['state'] = tk.DISABLED


botao_fotografar = tk.Button(janela, text = "Fotografar",font = ('arial',8), command = fotografar)
botao_fotografar.place(x = 453, y = 36)

botao_upload = tk.Button(janela, text = "Enviar", command = envia_foto, state = 'disabled')
botao_upload.place(x = 462, y = 67)

#Braile
    #Etiqueta
# etiqueta_braile = tk.Label(janela, text = "Braile")
# etiqueta_braile.place(x = 15, y = 280)

    #Janela
janela_braile_externa = tk.Canvas(janela, background = "black", width = 533, height = 75)
janela_braile_externa.place(x = 10, y = 282)
janela_braile_interna = tk.Canvas(janela, background = "white", width = 523, height = 65)
janela_braile_interna.place(x = 15, y = 287)

    #Função auxiliar
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

# braile = "101110, 111110, 110101, 101101"

    #Trata braile //101}coluna 1, 110}coluna 2
if braile:
        #separa os digitos e transfoma para inteiro
    dig1 = int(braile[0:6])
    dig2 = int(braile[8:14])
    dig3 = int(braile[16:-8])
    dig4 = int(braile[-6:])
        
        #dicionário de digitos de dicionário de colunas de dicionário de bolas //cada bola diz seu estado 0 abaixada, 1 levantada
#     dicionario_braile = [('dig1',
#                           [('col1',
#                               [('bol1', int(dig1/100000)),
#                                ('bol2', int((dig1/10000))%10),
#                                ('bol3', int((dig1/1000))%10)]),
#                             ('col2',
#                              [('bol1', int((dig1/100))%10),
#                               ('bol2', int((dig1/10))%10),
#                               ('bol3', int(dig1%10))])]),
#                           
#                           ('dig2',
#                            [('col1',
#                              [('bol1', int(dig2/100000)),
#                               ('bol2', int((dig2/10000))%10),
#                               ('bol3', int((dig2/1000))%10)]),
#                             ('col2',
#                              [('bol1', int((dig2/100))%10),
#                               ('bol2', int((dig2/10))%10),
#                               ('bol3', int(dig2%10))])]),
#                           
#                           ('dig3',
#                            [('col1',
#                              [('bol1', int(dig3/100000)),
#                               ('bol2', int((dig3/10000))%10),
#                               ('bol3', int((dig3/1000))%10)]),
#                             ('col2',
#                              [('bol1', int((dig3/100))%10),
#                               ('bol2', int((dig3/10))%10),
#                               ('bol3', int(dig3%10))])]),
#                           
#                           ('dig4',
#                            [('col1',
#                              [('bol1', int(dig4/100000)),
#                               ('bol2', int((dig4/10000))%10),
#                               ('bol3', int((dig4/1000))%10)]),
#                             ('col2',
#                              [('bol1', int((dig4/100))%10),
#                               ('bol2', int((dig4/10))%10),
#                               ('bol3', int(dig4%10))])])]
#     

    #Desenho da estrutura do braile
    #//fill = white -> 0/false, fill = black -> 1/true
def desenha_bolas_braile():
        #variáveis de desenho
    x_coluna1 = 14
    x_coluna2 = x_coluna1 + 15
    y1 = 13
    y2 = y1 + 15
    y3 = y2 + 15
    distancia_digito = 44
    
        #variável do loop 
    digito = 0
     
    while digito < 12:
            #digito n
                #coluna 1
        janela_braile_interna.create_circle(x_coluna1+distancia_digito*digito, y1, 4, fill = "white", outline = "grey", width = 1)
        janela_braile_interna.create_circle(x_coluna1+distancia_digito*digito, y2, 4, fill = "white", outline = "grey", width = 1)
        janela_braile_interna.create_circle(x_coluna1+distancia_digito*digito, y3, 4, fill = "white", outline = "grey", width = 1)

                #coluna 2
        janela_braile_interna.create_circle(x_coluna2+distancia_digito*digito, y1, 4, fill = "white", outline = "grey", width = 1)
        janela_braile_interna.create_circle(x_coluna2+distancia_digito*digito, y2, 4, fill = "white", outline = "grey", width = 1)
        janela_braile_interna.create_circle(x_coluna2+distancia_digito*digito, y3, 4, fill = "white", outline = "grey", width = 1)
        
        janela_braile_interna.create_text(x_coluna1+8+distancia_digito*digito, y3+15, text = "-", font = 3)
                
        digito += 1

desenha_bolas_braile()

    #Exibe braile
# def exibe_braile():
#         #variáveis de desenho
#     x_coluna1 = 14
#     x_coluna2 = x_coluna1 + 15
#     y1 = 13
#     y2 = y1 + 15
#     y3 = y2 + 15
#     distancia_digito = 44
#     
#         #variável do loop 
#     digito = 0
#      
#     while digito < 12:
#         #digito n
#             #coluna 1
#         janela_braile_interna.create_circle(x_coluna1+distancia_digito*digito, y1, 4, fill = "black", outline = "grey", width = 1)
#         janela_braile_interna.create_circle(x_coluna1+distancia_digito*digito, y2, 4, fill = "black", outline = "grey", width = 1)
#         janela_braile_interna.create_circle(x_coluna1+distancia_digito*digito, y3, 4, fill = "black", outline = "grey", width = 1)
# 
#             #coluna 2
#         janela_braile_interna.create_circle(x_coluna2+distancia_digito*digito, y1, 4, fill = "black", outline = "grey", width = 1)
#         janela_braile_interna.create_circle(x_coluna2+distancia_digito*digito, y2, 4, fill = "black", outline = "grey", width = 1)
#         janela_braile_interna.create_circle(x_coluna2+distancia_digito*digito, y3, 4, fill = "black", outline = "grey", width = 1)
#         
#         janela_braile_interna.create_text(x_coluna1+8+distancia_digito*digito, y3+15, text = "-", font = 3, fill = "white")
#         janela_braile_interna.create_text(x_coluna1+8+distancia_digito*digito, y3+15, text = "a", font = 3)
# 
#         digito += 1
# 
# exibe_braile()

#Lop para exibir a stream
while True:
    video = stream.read()[1]
    video = cv.flip(video, 1)
    video_tratado = cv.cvtColor(video, cv.COLOR_BGR2RGB)
    video = ImageTk.PhotoImage(Image.fromarray(video_tratado))
    painel_foto.config(image = video, width = 400, height = 257)
    painel_foto.image = video
    janela.update()
    
stream.release()
cv.destroyAllWindows()

janela.tk.mainloop()
