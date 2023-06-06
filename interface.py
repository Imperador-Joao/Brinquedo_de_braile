#Bibliotecas
import tkinter as tk
from PIL import ImageTk, Image
from serial import Serial
from os import system
from requests import get, post
from datetime import datetime, timedelta

#Variáveis globais
global imagem, path
global painel_foto, etiqueta_foto
global palavra

#Inicia serial
#meu_serial = Serial("COM26", baudrate = 9600, timeout = 0.1)

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
janela_botoes = tk.Canvas(janela, background = "black", width = 123, height = 95)
janela_botoes.place(x = 420, y = 15)
janela_botoes2 = tk.Canvas(janela, background = "grey93", width = 113, height = 85)
janela_botoes2.place(x = 425, y = 20)

    #Fotografar
def tira_foto():
    global imagem, path
    
        #captura imagem
    data_foto = str(datetime.now()).replace(" ","-")
    
        #envia comando para o sistema
#     comando_win = "CommandCam /filename " + data_foto + ".jpg /delay 500"
    comando_lin = "fswebcam --resolution 640x480 --skip 10 " + data_foto + ".jpg"
#     system(comando_win)
    system(comando_lin)
    
    print("Tirei foto!")
    
    path = data_foto + ".jpg"
#     path = "foto_telegram.jpg"
    
        #abrir imagem
    imagem = Image.open(path)
    
        #redimenciona
    redimencionada = imagem.resize((400, 255), Image.LANCZOS)
        
        #projeta
    nova_imagem = ImageTk.PhotoImage(redimencionada)
    painel_foto.config(image = nova_imagem, width = 400, height = 255)
    painel_foto.image = nova_imagem
    
        #destroi Label de texto
    etiqueta_foto.destroy()

        #ativa botão de upload
    botao_upload['state'] = tk.NORMAL

botao_fotografar = tk.Button(janela, text = "Fotografar", command = tira_foto)
botao_fotografar.place(x = 450, y = 35)

    #Upload
def envia_foto():
    global etiqueta_foto, palavra
    print("Enviando pros deuses")
    
        #enviar foto para o identificador
            #dados da conversa
    chave = "6296661403:AAFru8mD_bctyb56n4PkObmyVJXHhvSPkv4"
    endereco_base = "https://api.telegram.org/bot" + chave
    endereco_dados_do_bot = endereco_base + "/getMe"
    id_da_conversa = "2040258692"    
    endereco_para_foto = endereco_base + "/sendPhoto"
    
            #envio
    dados_envio = {"chat_id": id_da_conversa}
    arquivo_envio = {"photo": open(path, "rb")}
    resultado_envio = post(endereco_para_foto, data = dados_envio, files = arquivo_envio)
    print(resultado_envio.text)
    
        #recebe json //só recebe uma vez, a cada upload
    endereco_resposta = endereco_base + "/getUpdates"
    dados_resposta = {"offset": proximo_id_de_update}
    
    print("\nBuscando novas mensagens...")
    resposta = get(endereco_resposta, json = dados_resposta)
    dicionario_resposta = resposta.json()
    
        #trata json //pega aprimeira mensagem de texto (deve ser uma palavra)
    for resultado in dicionario_da_resposta["result"]:
        mensagem = resultado["message"]
        
        if "text" in mensagem:
            palavra = mensagem["text"]
            
        #envia a palavra para o arduino
#     palavra_chave = palavra + "\n"
#     meu_serial.write(palavra_chave.encode("UFT-8"))
    
        #muda janela foto para o padão
    imagem_grey = tk.PhotoImage("grey.jpg")
    painel_foto.config(image = imagem_grey, width = 400, height = 255)
    painel_foto.image = imagem_grey
    etiqueta_foto = tk.Label(janela, text = "Tire uma foto", fg = "white" , bg = "grey")
    etiqueta_foto.place(x = 176, y = 135)
    
        #desativa botão de upload
    botao_upload['state'] = tk.DISABLED

botao_upload = tk.Button(janela, text = "Upload", command = envia_foto, state = 'disabled')
botao_upload.place(x = 457, y = 65)

#Braile
    #Etiqueta
etiqueta_braile = tk.Label(janela, text = "Braile")
etiqueta_braile.place(x = 15, y = 280)

    #Janela
janela_braile = tk.Canvas(janela, background = "white", width = 525, height = 185)
janela_braile.place(x = 10, y = 300)

    #Bolas //engrenagem, coluna, bola, preta/branca
e1c1b1p = tk.Canvas(janela, width = 20, height = 20)
e1c1b1p.place(x = 20, y = 350)
e1c1b1p.create_oval(100, 100, 300, 300)

    #Importa braile


    #Trata braile //101}coluna 1, 110}coluna 2
braile = "101110, 111110, 110101, 101101"
#if braile:
    
    #Exibe braile

#Funções auxiliares


janela.tk.mainloop()
