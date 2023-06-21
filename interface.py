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
global lista_palavras

lista_palavras = ['Garrafa', 'Eletrônico', 'b', 'aaaaaaaaaaaaaaaaaaaa', 'aabaaaa', 'aaabaaaa', 'aaabaaa', 'aaabaaaaa']
    
#Inicia serial
#meu_serial = Serial("COM26", baudrate = 9600, timeout = 0.1)

#Inicia vídeo
stream = cv.VideoCapture(0)
if (stream.isOpened() == False):
  print("Câmera não encontrada")

#Chave amozon
with open('reconhecimento/ChavesAcesso.csv','r') as credenciais:
    next(credenciais)
    chave,senha = list(csv.reader(credenciais))[0]

#Criação da janela
janela = tk.Tk()
janela.title("Interface")
janela.geometry("908x376")

#Janelas
    #Foto
painel_foto = tk.Label(janela, background = "grey", width = 57, height = 17)
painel_foto.place(x = 12, y = 17)

    #Estato
janela_estato_externa = tk.Canvas(janela, background = "black", width = 123, height = 160)
janela_estato_externa.place(x = 420, y = 116)
janela_estato_interna = tk.Canvas(janela, background = "grey93", width = 113, height = 150)
janela_estato_interna.place(x = 425, y = 121)
janela_estato_interna.create_text(55, 35, text = "Palavra:", font = 1)
estado_atual_palavra = tk.Label(janela, background = "grey93", text = "Fotografe!", font = 1)
estado_atual_palavra.place(x = 440, y = 123)
etiqueta_palavra = tk.Label(janela, text = "", bg = 'grey93')
etiqueta_palavra.place(x = 455, y = 170)

    #Botões
janela_botoes_interno = tk.Canvas(janela, background = "black", width = 123, height = 95)
janela_botoes_interno.place(x = 420, y = 15)
janela_botoes_externo = tk.Canvas(janela, background = "grey93", width = 113, height = 85)
janela_botoes_externo.place(x = 425, y = 20)

    #Listbox
lb_palavras = tk.Listbox(janela, bd = 4, width = 22, height = 13, justify = tk.CENTER)
for palavra in lista_palavras:
    lb_palavras.insert(tk.END, palavra)
lb_palavras.place(x = 548, y = 16)

#Botões
    #Funções
        #Adiciona palavra na lista
def adiciona_palavra_lista():
    global lista_palavras

            #pega palavara
    palavra_adicionada = entrada_nova_palavra.get()
    
            #adiciona na interface
    lb_palavras.insert(tk.END, palavra_adicionada)
    
            #adiciona na lista
    lista_palavras.append(str(palavra_adicionada))
    print(lista_palavras)
    
        #Traduzir palavra da lista
def traduzir_palavra_lista():
    global braile, palavra_traduzida
    
            #pega palavra selecionada
    palavra_selecionada = lb_palavras.get(tk.ACTIVE)
    
            #traduz pra braile
    braile = escrever_braile(unidecode(str(palavra_selecionada)))
    
            #desenha braile
    palavra_traduzida = str(palavra_selecionada)
    preeche_braile()
    
        #Deletar palavra da lista
def deletar_palavra_lista():
    global lista_palavras
    
            #deleta palavra selecionada
    lb_palavras.delete(tk.ACTIVE)
    
            #retira da lista
    lista_palavras.remove(str(lb_palavras.get(tk.ACTIVE)))
    print("==removido=="+str(lista_palavras))

        #Envia string de palavras para salvar no arduino
def salva_arduino():
    global meu_serial, braile, palavra_traduzida
        
            #envia sinal para o arduino
#     meu_serial.write("1Salva")
    
        #Fotografar
def fotografar():
    global imagem, nome_arquivo_foto, etiqueta_palavra
    
            #tira foto
    imagem = Image.fromarray(video_tratado) 
    nome_arquivo_foto = datetime.now().strftime('Foto_teste_%d_%m_%y__%H_%M_%S.jpg')    
    imagem.save("Fotos/"+nome_arquivo_foto)

#     tirar_foto(nome = data_foto,sistema_operacional = sistema_operacional)
    
    print("Tirei foto!")

            #ativa botão de upload
    botao_upload['state'] = tk.NORMAL
    
            #altera palavra estado atual
    estado_atual_palavra.config(text = "Envie!")
    estado_atual_palavra.place(x = 455, y = 123)
    
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
    etiqueta_palavra.place(x = 435, y = 165)

            #envia palavra traduzida e braile pro arduino "bala","100100,200220,300300,400400"
    palavra_arduino = '"{}",'.format(palavra_traduzida)
    for lista_digito in braile:
        for lista_coluna in lista_digito:
            for bola in lista_coluna:
                palavra_arduino += str(bola)
                
        palavra_arduino += ','

    palavra_arduino += '"'
    
    print("=palavra="+palavra_arduino)
#     palavra_arduino = '"' + palavra_traduzida + '","' + str(braile).replace('[', '').replace(']', '').replace(' ', '') + '"\n' REFAZER!!!
#     print(palavra_arduino)
#     meu_serial.write(palavra_arduino.encode("UTF-8"))

            #exibe brile
    preeche_braile()
    
            #altera estado atual
    estado_atual_palavra.config(text = "Fotografe!")
    estado_atual_palavra.place(x = 440, y = 123)
    
            #desativa botão de upload
    botao_upload['state'] = tk.DISABLED

    #Posicionar botões
        #Fotografar
botao_fotografar = tk.Button(janela, text = "Fotografar",font = ('arial',8), command = fotografar)
botao_fotografar.place(x = 453, y = 23)

        #Enviar
botao_upload = tk.Button(janela, text = "Enviar", command = envia_foto, state = 'disabled')
botao_upload.place(x = 462, y = 51)

        #Adicionar
botao_adicionar = tk.Button(janela, text = "Adicionar", command = adiciona_palavra_lista)
botao_adicionar.place(x = 453, y = 230)

            #Entrada
entrada_nova_palavra = tk.Entry(janela,text = "Palavra de 12 letras", width = 18)
entrada_nova_palavra.place(x = 427, y = 205)

        #Traduzir
botao_traduzir = tk.Button(janela, text = "Traduzir", command = traduzir_palavra_lista)
botao_traduzir.place(x = 565, y = 245)

        #Deletar
botao_traduzir = tk.Button(janela, text = "Deletar", command = deletar_palavra_lista)
botao_traduzir.place(x = 625, y = 245)

        #Salvar
botao_salvar = tk.Button(janela, text = "Salvar", command = salva_arduino)
botao_salvar.place(x = 462, y = 80)

#Braile
    #Janela
janela_braile_externa = tk.Canvas(janela, background = "black", width = 885, height = 76)
janela_braile_externa.place(x = 10, y = 282)
janela_braile_interna = tk.Canvas(janela, background = "grey93", width = 875, height = 66)
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
    y1 = 14
    y2 = y1 + 15
    y3 = y2 + 15
    distancia_digito = 44
    
        #variável do loop 
    digito = 0
    
    #"apaga" digitos anteriores
    janela_braile_interna.create_rectangle(18, 54, 18+845, 54+12, fill = "grey93", outline = "grey93")
    
    while digito < 20:
            #digito n
                #coluna 1
        janela_braile_interna.create_circle(x_coluna1+distancia_digito*digito, y1, 4, fill = "grey93", outline = "grey", width = 1)
        janela_braile_interna.create_circle(x_coluna1+distancia_digito*digito, y2, 4, fill = "grey93", outline = "grey", width = 1)
        janela_braile_interna.create_circle(x_coluna1+distancia_digito*digito, y3, 4, fill = "grey93", outline = "grey", width = 1)

                #coluna 2
        janela_braile_interna.create_circle(x_coluna2+distancia_digito*digito, y1, 4, fill = "grey93", outline = "grey", width = 1)
        janela_braile_interna.create_circle(x_coluna2+distancia_digito*digito, y2, 4, fill = "grey93", outline = "grey", width = 1)
        janela_braile_interna.create_circle(x_coluna2+distancia_digito*digito, y3, 4, fill = "grey93", outline = "grey", width = 1)
                
        digito += 1

desenha_braile()

    #Exibe braile
def preeche_braile():
    global braile, palavra_traduzida
    
        #variáveis de desenho
    x_coluna1 = 14
    x_coluna2 = x_coluna1 + 15
    y1 = 14
    y2 = y1 + 15
    y3 = y2 + 15
    distancia_digito = 44
    
        #variáveis do loop 
    digito = 0
    coluna = 0
    bola = 0
    
        #"apaga" digitos anteriores
    desenha_braile()
    
    while digito < len(braile):
        #ignora espaços em branco
        if braile[digito] == None:
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
