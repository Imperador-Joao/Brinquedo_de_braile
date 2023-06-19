from googletrans import Translator
# Baixar versão 3.1.0a0

LETRAS = [chr(i) for i in range(97,123)]
LADO = {0:[0,0,0],
        1:[0,0,1],
        2:[0,1,0],
        3:[1,0,0],
        4:[1,1,0],
        5:[1,0,1],
        6:[0,1,1],
        7:[1,1,1]}

'''
BRAILE = [[LADO[1],LADO[0]],
          [LADO[3],LADO[0]],
          [LADO[1],LADO[1]],
          [LADO[1],LADO[3]],
          [LADO[1],LADO[2]],
          [LADO[3],LADO[1]],
          [LADO[3],LADO[3]],
          [LADO[3],LADO[2]],
          [LADO[2],LADO[1]],
          [LADO[2],LADO[3]],
          [LADO[-3],LADO[0]],
          [LADO[-1],LADO[0]],
          [LADO[-3],LADO[1]],
          [LADO[-3],LADO[3]],
          [LADO[-3],LADO[2]],
          [LADO[-1],LADO[1]],
          [LADO[-1],LADO[3]],
          [LADO[-1],LADO[2]],
          [LADO[-2],LADO[1]],
          [LADO[-2],LADO[3]],
          [LADO[-3],LADO[-4]],
          [LADO[-1],LADO[-4]],
          [LADO[2],LADO[-1]],
          [LADO[-3],LADO[-3]],
          [LADO[-3],LADO[-1]],
          [LADO[-3],LADO[-2]]]
'''

BRAILE = [[[1, 0, 0], [0, 0, 0]], [[1, 1, 0], [0, 0, 0]], [[1, 0, 0], [1, 0, 0]],
           [[1, 0, 0], [1, 1, 0]], [[1, 0, 0], [0, 1, 0]], [[1, 1, 0], [1, 0, 0]],
           [[1, 1, 0], [1, 1, 0]], [[1, 1, 0], [0, 1, 0]], [[0, 1, 0], [1, 0, 0]],
           [[0, 1, 0], [1, 1, 0]], [[1, 0, 1], [0, 0, 0]], [[1, 1, 1], [0, 0, 0]],
           [[1, 0, 1], [1, 0, 0]], [[1, 0, 1], [1, 1, 0]], [[1, 0, 1], [0, 1, 0]],
           [[1, 1, 1], [1, 0, 0]], [[1, 1, 1], [1, 1, 0]], [[1, 1, 1], [0, 1, 0]],
           [[0, 1, 1], [1, 0, 0]], [[0, 1, 1], [1, 1, 0]], [[1, 0, 1], [0, 0, 1]],
           [[1, 1, 1], [0, 0, 1]], [[0, 1, 0], [1, 1, 1]], [[1, 0, 1], [1, 0, 1]],
           [[1, 0, 1], [1, 1, 1]], [[1, 0, 1], [0, 1, 1]]]


DICIONARIO_LETRA_BRAILE = dict(zip(LETRAS,BRAILE))


def traduzir(texto, idioma_origem = 'en', idioma_destino = 'pt'):
    tradutor = Translator()
    traducao = tradutor.translate(texto, src = idioma_origem, dest = idioma_destino)
    return traducao.text

def escrever_braile(texto):
    
    return [DICIONARIO_LETRA_BRAILE.get(letra.lower()) for letra in texto]
