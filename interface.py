#Bibliotecas
import tkinter as tk
from PIL import ImageTk, Image
from serial import Serial
import cv2 as cv
from requests import get, post
from datetime import datetime, timedelta
import csv
from unidecode import unidecode
from utilitarios.dicionario import traduzir, escrever_braile
from reconhecimento.detector import tirar_foto, Detector_aws

#Variáveis globais
global imagem, nome_arquivo_foto
global painel_foto, estado_atual_palavra, etiqueta_palavra
global braile, palavra_traduzida
global meu_serial

#Inicia serial
#meu_serial = Serial("COM26", baudrate = 9600, timeout = 0.1)

#Inicia vídeo
stream = cv.VideoCapture(0)
if (stream.isOpened() == False):
  print("Câmera não encontrada")

#Chave amozon
with open('C:/Users/micro2/Downloads/Brinquedo_de_braile-main/reconhecimento/ChavesAcesso.csv','r') as credenciais:
    next(credenciais)
    chave,senha = list(csv.reader(credenciais))[0]

#Criação da janela
janela = tk.Tk()
janela.title("Interface")
janela.geometry("557x376")

#Janela foto
painel_foto = tk.Label(janela, background = "grey", width = 57, height = 17)
painel_foto.place(x = 12, y = 17)

#Janela palavra
janela_botoes_externa = tk.Canvas(janela, background = "black", width = 123, height = 160)
janela_botoes_externa.place(x = 420, y = 116)
janela_botoes_interna = tk.Canvas(janela, background = "grey93", width = 113, height = 150)
janela_botoes_interna.place(x = 425, y = 121)
janela_botoes_interna.create_text(55, 70, text = "Palavra:", font = 1)
estado_atual_palavra = tk.Label(janela, background = "grey93", text = "Fotografe!", font = 1)
estado_atual_palavra.place(x = 440, y = 135)

#Botões
    #Janela

janela_botoes_interno = tk.Canvas(janela, background = "black", width = 123, height = 95)
janela_botoes_interno.place(x = 420, y = 15)
janela_botoes_externo = tk.Canvas(janela, background = "grey93", width = 113, height = 85)
janela_botoes_externo.place(x = 425, y = 20)

    #Fotografar
def fotografar():
    global imagem, nome_arquivo_foto, etiqueta_palavra
    
        #tira foto
    imagem = Image.fromarray(video_tratado) 
    nome_arquivo_foto = datetime.now().strftime('Foto_teste_%d_%m_%y__%H_%M_%S.jpg')    
    imagem.save(nome_arquivo_foto)

#     tirar_foto(nome = data_foto,sistema_operacional = sistema_operacional)
    
    print("Tirei foto!")

        #ativa botão de upload
    botao_upload['state'] = tk.NORMAL
    
    #altera palavra estado atual
    estado_atual_palavra.config(text = "Envie!")
    estado_atual_palavra.place(x = 455, y = 135)
    
    etiqueta_palavra.config(text = "")
    
    desenha_braile()

    #Upload
def envia_foto():
    global meu_serial, nome_arquivo_foto, braile, palavra_traduzida, estado_atual_palavra, etiqueta_palavra
    print("Enviando para a IA")
    
        #enviar foto para o identificador da amazon
    detector_amazon = Detector_aws(senha = senha, chave = chave)
    with open(nome_arquivo_foto,'rb') as imagem_fonte:
        bytes_fonte = imagem_fonte.read()
    
        #recebe itens detectados
    itens_detectados = detector_amazon.receber_dados(bytes_imagem = bytes_fonte, etiquetas = 8).get('Labels')

        #separa palavra com maior confiança
    palavra_maior_confianca = itens_detectados[0].get('Name')
    
        #traduz palavra
            #en -> pt-br
    palavra_traduzida = traduzir(texto=palavra_maior_confianca)
    
            #pt-br -> braile
    braile = escrever_braile(unidecode(palavra_traduzida))
    print(braile)
        #exibe palavra traduzida
    etiqueta_palavra = tk.Label(janela, text = palavra_traduzida, bg = 'grey93')
    etiqueta_palavra.place(x = 450, y = 200)

        #envia palavra traduzida e braile pro arduino
#     palavra_arduino = '"' + palavra_traduzida + '","' + str(braile).replace('[', '').replace(']', '').replace(' ', '') + '"\n' REFAZER!!!
    print(palavra_arduino)
#     meu_serial.write(palavra_arduino.encode("UTF-8"))

        #exibe brile
    preeche_braile()
    
        #altera estado atual
    estado_atual_palavra.config(text = "Fotografe!")
    estado_atual_palavra.place(x = 440, y = 135)
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

    #Desenho da estrutura do braile
    #//fill = white -> 0/false, fill = black -> 1/true
def desenha_braile():
        #variáveis de desenho
    x_coluna1 = 14
    x_coluna2 = x_coluna1 + 15
    y1 = 13
    y2 = y1 + 15
    y3 = y2 + 15
    distancia_digito = 44
    
        #variável do loop 
    digito = 0
    
    #"apaga" digitos anteriores
    janela_braile_interna.create_rectangle(18, 54, 18+495, 54+10, fill = "white", outline = "white")    
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

desenha_braile()

    #Exibe braile
def preeche_braile():
    global braile, palavra_traduzida
    
        #variáveis de desenho
    x_coluna1 = 14
    x_coluna2 = x_coluna1 + 15
    y1 = 13
    y2 = y1 + 15
    y3 = y2 + 15
    distancia_digito = 44
    
        #variáveis do loop 
    digito = 0
    coluna = 0
    bola = 0
    
        #"apaga" digitos anteriores
    janela_braile_interna.create_rectangle(18, 54, 18+495, 54+10, fill = "white", outline = "white")
    
    while digito < len(braile):
        if braile[digito] == 'Nome':
            digito += 1
            
        while coluna < 2:
            if coluna == 0: #desenha na primeira coluna
                while bola < 3:
                    if braile[digito][coluna][bola] == 1:
                        if bola == 0: #desenha bola do topo
                            janela_braile_interna.create_circle(x_coluna1+distancia_digito*digito, y1, 4, fill = "black", outline = "grey", width = 1)

                        elif bola == 1: #desenha bola do meio
                            janela_braile_interna.create_circle(x_coluna1+distancia_digito*digito, y2, 4, fill = "black", outline = "grey", width = 1)

                        else: #desenha bola de baixo
                            janela_braile_interna.create_circle(x_coluna1+distancia_digito*digito, y3, 4, fill = "black", outline = "grey", width = 1)

                    bola += 1
                        
            else: #desenha na segunda coluna         
                while bola < 3:
                    if braile[digito][coluna][bola] == 1:
                        if bola == 0: #desenha bola do topo
                            janela_braile_interna.create_circle(x_coluna2+distancia_digito*digito, y1, 4, fill = "black", outline = "grey", width = 1)
                                
                        elif bola == 1: #desenha bola do meio
                            janela_braile_interna.create_circle(x_coluna2+distancia_digito*digito, y2, 4, fill = "black", outline = "grey", width = 1)

                        else: #desenha bola de baixo
                            janela_braile_interna.create_circle(x_coluna2+distancia_digito*digito, y3, 4, fill = "black", outline = "grey", width = 1)

                    bola += 1
                    
            coluna += 1
            bola = 0
        
        janela_braile_interna.create_text(x_coluna1+8+distancia_digito*digito, y3+15, text = palavra_traduzida[digito])
        digito += 1
        coluna = 0
        bola = 0

# preeche_braile()

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
