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
    redimencionada = imagem.resize((400, 257), Image.LANCZOS)
        
        #projeta
    nova_imagem = ImageTk.PhotoImage(redimencionada)
    painel_foto.config(image = nova_imagem, width = 400, height = 257)
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
    painel_foto.config(image = imagem_grey, width = 400, height = 257)
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
