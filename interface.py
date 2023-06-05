import tkinter as tk
from PIL import ImageTk, Image
from serial import Serial
from os import system
from subprocess import Popen
from requests import get, post
from datetime import datetime, timedelta

global data_foto

#Criação da janela
janela = tk.Tk()
janela.title("Interface")
janela.geometry("550x500")

#Janela foto
janela_braile = tk.Canvas(janela, background = "grey", width = 400, height = 260)
janela_braile.place(x = 10, y = 15)

#Botões
    #Fotografar
def tira_foto():
        #captura imagem
    global data_foto
    data_foto = datetime.now()
    
    #comando_win = "CommandCam /filename " + str(data_foto) + ".jpg /delay 500"
    comando_lin = f"fswebcam --resolution 640x480 --skip 10{data_foto}.jpg"
    
    #system(comando_win)
    system(comando_lin)
    
    print("Tirei foto!")
    
    exibe_foto()
    
        #ativa botão de upload
    botao_upload['state'] = tk.NORMAL

botao_fotografar = tk.Button(janela, text = "Fotografar", command = tira_foto)
botao_fotografar.place(x = 430, y = 15)

    #Upload
def envia_foto():
    print("Enviando pros deuses")

        #desativa botão de upload
    botao_upload['state'] = tk.DISABLED

botao_upload = tk.Button(janela, text = "Upload", command = envia_foto, state = 'disabled')
botao_upload.place(x = 430, y = 45)

#Braile
    #Etiqueta
etiqueta_braile = tk.Label(janela, text = "Braile")
etiqueta_braile.place(x = 15, y = 280)

    #Janela
janela_braile = tk.Canvas(janela, background = "white", width = 525, height = 185)
janela_braile.place(x = 10, y = 300)

    #Importa braile
#braile = serial.Serial("porta", 9600, timeout = 0.5)

    #Trata braile


    #Exibe braile

#Funções auxiliares
    #Exibe imagem
def exibe_foto():
#   global data_foto
#	path = str(data_foto) + ".jpg"
    path = "foto_telegram.jpg"
    
        #abrir imagem
    imagem = Image.open(path)
    
        #redimencioando
    redimencionada = imagem.resize((400, 260), Image.LANCZOS)
        
        #projetando
    nova_imagem = ImageTk.PhotoImage(redimencionada)
    painel = tk.Label(janela, image = nova_imagem)
    painel.place(x = 10, y = 15)



janela.mainloop()
