from os import system
import boto3


def tirar_foto(nome = 'foto_camera',sistema_operacional = 'Linux'):

    argumentos = {'Linux': f"fswebcam --resolution 640x480 --skip 10 {nome}.jpg",
                  'Windows':f"CommandCam /filename {nome}.jpg /delay 500"}

    argumento_sistema = argumentos.get(sistema_operacional)
    system(argumento_sistema)

    '''
    resposta = input('A foto ficou boa?\t')

    if resposta.lower() != 'sim':
        tirar_foto(nome)
    '''
    
class Detector_aws:

    def __init__(self,chave,senha):

        self.cliente = boto3.client('rekognition',
                       aws_access_key_id = chave,
                       aws_secret_access_key = senha,
                       region_name = 'eu-central-1')

        return
    
    def receber_dados(self,bytes_imagem,etiquetas = 5):

        return self.cliente.detect_labels(Image = {'Bytes':bytes_imagem},MaxLabels = etiquetas)
    