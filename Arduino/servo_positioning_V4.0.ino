//ENG1419_PROJETO_FINAL -> Brinquedo Braile

//Premissa inicial
//montagem de dois servos + programa em Arduino que recebe código braile pela serial e gira servos de acordo
#include "Arduino.h"
#include "DFRobotDFPlayerMini.h"
#include <EEPROM.h>
#include <GFButton.h>
#include <Servo.h>
#include <ShiftDisplay.h>
#include "SoftwareSerial.h"


// Botoes
GFButton botaoPalavras(A1);

GFButton botaoLetra1(A8);
GFButton botaoLetra2(A9);
GFButton botaoLetra3(A10);
GFButton botaoLetra4(A11);

GFButton sensor(A12);

int indiceLetraGlobal = 0;

int potenciometroVolume = A7;
int volume;

int rclk = 4;
int sclk = 3;
int dio = 2;
int indicesDisplay[] = { 3, 2, 1, 0 };

unsigned long tempoAnteriorSensor;

String texto;
DFRobotDFPlayerMini myDFPlayer;
ShiftDisplay display(rclk, sclk, dio, COMMON_ANODE, 4, true, indicesDisplay);

struct servoPos {
  Servo servoVar;
  String posDes;  //Define a posicao do servo
  int posFinal;   //Variavel para acompanhar a posicao dos servos (1,2,3...8)
  //Ex: TagBraile[0] -> 1o caracter em Braile, sera possivel garantir que apenas servo 1 e servo 2 atuem para o braile 1.
};

servoPos servoPos1;
servoPos servoPos2;
servoPos servoPos3;
servoPos servoPos4;
servoPos servoPos5;
servoPos servoPos6;
servoPos servoPos7;
servoPos servoPos8;

servoPos listaDeServos[] = { servoPos1, servoPos2, servoPos3, servoPos4, servoPos5, servoPos6, servoPos7, servoPos8 };

struct sorteioPalavras {
  char palavra[21];
  char braile[150];
};

//20 palavras
sorteioPalavras *listaDeSorteios = {};
/*=
  {
  {"Batata", "110000,100000,011110,100000,011110,100000"},
  {"TV", "011110,111001"},
  {"Cama", "100100,100000,101100,100000"},
  {"Pipoca", "111100,010100,111100,101010,100100,100000"},
  {"Mesa", "101100,100010,011100,100000"},
  {"Agua", "100000,110110,101001,100000"},
  {"Teclado", "011110,100010,100100,111000,100000,100110,101010"},
  {"Mouse", "101100,101010,101001,011100,100010"},
  {"Caneta", "100100,100000,101110,100010,011110,101010"},
  {"Cadeira", "100100,101010,100110,100010,010100,111010,100000"},
  {"Abacate", "100000,110000,100000,100100,100000,011110,100010"},
  {"Pessoa", "111100,100010,011100,011100,101010,100000"},
  {"Robo", "111010,101010,110000,101010"},
  {"Carro", "100100,100000,111010,111010,101010"},
  {"Ameixa", "100000,101100,100010,010100,101101,100000"},
  {"Bomba", "110000,101010,101100,110000,100000"},
  {"Lagarto", "111000,100000,110110,100000,111010,011110,101010"},
  {"Cao", "100100,100000,101010"},
  {"Passaro", "111100,100000,011100,011100,100000,111010,101010"}, // P A S S A R O
  {"Tinta", "011110,010100,101110,011110,100000"},// T I N T A
  };
*/

struct posDinamicaServo
{
  unsigned long instanteServos;
  int posAtual;
};

posDinamicaServo posDinamicaServo1;
posDinamicaServo posDinamicaServo2;
posDinamicaServo posDinamicaServo3;
posDinamicaServo posDinamicaServo4;
posDinamicaServo posDinamicaServo5;
posDinamicaServo posDinamicaServo6;
posDinamicaServo posDinamicaServo7;
posDinamicaServo posDinamicaServo8;

posDinamicaServo listaServoDinamPos[] = { posDinamicaServo1, posDinamicaServo2, posDinamicaServo3, posDinamicaServo4, posDinamicaServo5, posDinamicaServo6, posDinamicaServo7, posDinamicaServo8};

int braileTag = 0;    //Variavel para facilitar a correlacao de movimentos dos servos (1,2,3 ou 4)
int braileStart = 0;  //Referencial do começo do serial para substring.
int i = 0;
int saveRng = 0;

int velFinal1;
int velFinal2;
int velAtual1 = 0;
int velAtual2 = 0;

bool eLista = false;
bool eFoto = false;

int posicaoLista = 0;
int qtd_palavras = 0;

unsigned long instanteAnterior = 0;

void setup() 
{
  // Inicializando a comunicacao serial.
  Serial.begin(115200);
  Serial1.begin(9600);
  
  botaoPalavras.setReleaseHandler(sorteia);
  
  botaoLetra1.setReleaseHandler(funcaoBotao1);
  botaoLetra2.setReleaseHandler(funcaoBotao2);
  botaoLetra3.setReleaseHandler(funcaoBotao3);
  botaoLetra4.setReleaseHandler(funcaoBotao4);
  
  sensor.setReleaseHandler(funcaoSensor);
   //SoftwareSerial mySoftwareSerial(19, 18); // RX, TX
  
  //EEPROM.put(0,0);
  EEPROM.get(0, qtd_palavras);
  Serial.println(qtd_palavras);

  if (qtd_palavras > 0) 
  {
    listaDeSorteios = (sorteioPalavras *)malloc(sizeof(sorteioPalavras) * qtd_palavras);
    for (int j = 0; j < qtd_palavras; j++) 
    {
      EEPROM.get(2 + (j * sizeof(sorteioPalavras)), listaDeSorteios[j]);
    }
    for (int j = 0; j < qtd_palavras; j++) 
    {
      Serial.println(listaDeSorteios[j].palavra);
      Serial.println(listaDeSorteios[j].braile);
    }
  }
  randomSeed(analogRead(A0));  // Inicializa elemento aleatório
  

  for (i = 0; i < 8; i++)  //Inicializa todos os 8 servos
  {
    // Parametros do attach
    // [0] = pino ; [1] = comprimento minimo do pulso PWM (corresponde a 0 graus); [2] = comprimento maximo do pulso PWM (corresponde a 180 graus)
    listaDeServos[i].servoVar.attach(5 + i);
    //Serial.println(i);
  }
  
  if (!myDFPlayer.begin(Serial1)) {
    Serial.println(F("Nao inicializado:"));
    Serial.println(F("1.Cheque as conexoes do DFPlayer Mini"));
    Serial.println(F("2.Insira um cartao SD"));
  } else {
    Serial.println(F("Inicializado com sucesso:"));
    myDFPlayer.volume(19);
  }
  
  
  
}

int binToDec(String binario) {
  int decimal = 0;

  for (int i = 0; i < binario.length(); i++) {
    char digito = binario.charAt(i);
    if (digito == '0') {
      decimal = decimal * 2 + 0;
    } else if (digito == '1') {
      decimal = decimal * 2 + 1;
    }
  }
  return decimal;
}

void movimentaServo(int indiceServo) 
{
  int valor = 0;
  Serial.println(listaDeServos[indiceServo].posDes);
  valor = binToDec(listaDeServos[indiceServo].posDes);  // binario de 3 digitos -> valor de 0 a 7
  //Serial.println(servoEscolhido.posDes);
  Serial.print("Valor decimal: ");
  Serial.println(valor);
  //listaDeServoPos[indiceServo].posFinal = posicao;
  int posicaoGraus = 0;

  if (indiceServo % 2 == 0) 
  {
    posicaoGraus = 180 - (valor * 25.714);
  } else 
  {
    posicaoGraus = (valor * 25.714);
  }
  int difPos = posicaoGraus - listaServoDinamPos[indiceServo].posAtual;
  while (difPos != 0) 
  {
    if (millis() > listaServoDinamPos[indiceServo].instanteServos + 10) 
    {
      difPos = posicaoGraus - listaServoDinamPos[indiceServo].posAtual;
      if (difPos > 0)  
      {
        listaServoDinamPos[indiceServo].posAtual++;
      }
      if (difPos < 0) 
      {
        listaServoDinamPos[indiceServo].posAtual--;
      }

      listaServoDinamPos[indiceServo].instanteServos = millis();
    }
  
  listaDeServos[indiceServo].servoVar.write(listaServoDinamPos[indiceServo].posAtual);
  }
  listaDeServos[indiceServo].posFinal = listaServoDinamPos[indiceServo].posAtual;
  Serial.print("Angulo em graus final: ");
  Serial.println(listaDeServos[indiceServo].posFinal);
}

void sorteia(GFButton &botaoPalavras) {
  int randomNumber = random(qtd_palavras);
  Serial.println(qtd_palavras);
  Serial.println(randomNumber);
  Serial.println(listaDeSorteios[randomNumber].palavra);
  String message = String("Braile ") + String(listaDeSorteios[randomNumber].braile);
  Serial.println(message);
  leituraDeComando((String)listaDeSorteios[randomNumber].braile);
}



void leituraDeComando(String texto) {
  braileStart = 0;  //Indice inicial da sequencia Braile
  braileTag = 1;    //braileTag representa o par de motores que compõe o caracter Braile
  int indiceServo1 = 0;
  int indiceServo2 = 0;
  int quantidadeDeLoops = (texto.length()) / 6;
  Serial.println(quantidadeDeLoops);
  for (i = 0; i < quantidadeDeLoops; i++) {
    //&& (millis() - instanteAnterior) > 5000)
    //Através das funcoes abaixo é possível correlacionar o indice da lista de servos com a braileTag
    indiceServo1 = (2 * (braileTag - 1));  // 2*(1-1) = 0; 2*(2-1) = 2; 2*(3-1) = 4; 2*(4-1) = 6
    indiceServo2 = ((2 * braileTag) - 1);  // (2*1)-1 = 1; (2*2)-1 = 3; (2*3)-1 = 5; (2*4)-1 = 7
    listaDeServos[indiceServo1].posDes = texto.substring(braileStart, braileStart + 3);
    listaDeServos[indiceServo2].posDes = texto.substring(braileStart + 3, braileStart + 6);

    Serial.println("Enviando binario");
    Serial.print("Servo 1: ");
    Serial.print(listaDeServos[indiceServo1].posDes);
    Serial.print(",Servo 2 :");
    Serial.println(listaDeServos[indiceServo2].posDes);

    movimentaServo(indiceServo1);
    movimentaServo(indiceServo2);

    if (texto.charAt(braileStart + 6) == ',')  //Exemplo: chegou no caracter 8 -> braileTag = 2
    {
      Serial.println(texto.charAt(braileStart + 6));
      braileStart = braileStart + (6 + 1);  // Captura o digito logo após a virgula. Exemplo: Braile 001001,001001 CAPTUROU O '0'
      if (millis() > instanteAnterior + 5000)
      { 
        if (braileTag == 4) 
        {
          //sensorDeMovimento();
          instanteAnterior = millis();
          braileTag = 1;
          //delay(5000);
        } else {
          braileTag++;
        }
      }
    }
  }
}


void loop() {

  botaoPalavras.process();
  
  botaoLetra1.process();
  botaoLetra2.process();
  botaoLetra3.process();
  botaoLetra4.process();
  
  sensor.process();
  
  volume = map(analogRead(potenciometroVolume), 0, 1023, 0, 30);
  myDFPlayer.volume(volume);
  
  if (Serial.available() > 0) {
    String texto = Serial.readStringUntil('\n');
    texto.trim();

    //Codificao Braile -> 1 = * e 0 = -
    //Serial.println("HELLO TEXTO");
    //Serial.println(texto);
    indiceLetraGlobal = 0;
    //Primeiro Exemplo de Serial recebido: 1001001 -> O primeiro digito informa qual dos caracter braile do mecanismo deve representar, os seguintes 6 digitos as duas colunas que devem ser combinadas
    //Segundo Exemplo de Serial recebido: 3011101 -> Informação para o 3o caracter Braile -> _ * * * _ *

    /*
      Identifica string recebida
      primeiro vai receber "foto" ou "lista,num"
      vai verificar se as flags estão ativas(não de veriam estar), depois detecta na texto se é foto ou lista e torna ativa a sua respectiva flag

      segundo vai receber uma palavra seguida do seu braile, a unica respectiva à foto e a primeira respecvica à lista
      então vai entrar no seu respectivo if
    */
    if (eFoto)
     {
      //foto\n'abcte','000111,000101,010100'
      int indexVirgula_foto = texto.indexOf(",");
      String palavra_foto = texto.substring(1, indexVirgula_foto - 1);
      texto = texto.substring(indexVirgula_foto);
      String braile_foto = texto.substring(2, 	texto.indexOf("',"));  // mudar para 3 se tiver ,
      Serial.print("Palavra foto:");
      Serial.println(palavra_foto);
      Serial.print("Braile foto:");
      Serial.println(braile_foto);
      leituraDeComando(braile_foto);
      eFoto = false;
    }

    if (eLista) 
    {
      /*
        lista,3
        ,'chave','100100,110010,100000,111001,100010'
        ,'bala','110000,100000,111000,100000'
        ,'micro','101100,010100,100100,111010,101010'
      */
      /*lista,3 ,'chave','100100,110010,100000,111001,100010' ,'bala','110000,100000,111000,100000' ,'micro','101100,010100,100100,111010,101010'*/
      if (posicaoLista < qtd_palavras) {
        int indexVirgula_lista = texto.indexOf("',");
        strcpy(listaDeSorteios[posicaoLista].palavra, texto.substring(1, indexVirgula_lista).c_str());
        texto = texto.substring(indexVirgula_lista + 2);

        strcpy(listaDeSorteios[posicaoLista].braile, texto.substring(1, texto.lastIndexOf("'")).c_str());
        Serial.print("Palavra lista:");
        Serial.println(listaDeSorteios[posicaoLista].palavra);
        Serial.print("Braile lista:");
        Serial.println((String)listaDeSorteios[posicaoLista].braile);
        posicaoLista++;

        EEPROM.put(0, posicaoLista);
        for (int i = 0; i < posicaoLista; i++) {
          EEPROM.put(2 + (i * sizeof(sorteioPalavras)), listaDeSorteios[i]);
        }
      }

      else {
        eLista = false;
        posicaoLista = 0;
      }
    }

    if (texto.startsWith("foto")) eFoto = true;

    if (texto.startsWith("lista")) {
      EEPROM.put(0, 0);
      if (listaDeSorteios != NULL) free(listaDeSorteios);

      qtd_palavras = texto.substring(6, 7).toInt();
      listaDeSorteios = (sorteioPalavras *)malloc(sizeof(sorteioPalavras) * qtd_palavras);
      eLista = true;
    }
    if (texto.startsWith("calibrate")) 
    {
      String allServos_Zero= "000000,000000,000000,000000";
      leituraDeComando(allServos_Zero);
    }
  }
  display.set(texto.substring(indiceLetraGlobal));
  display.update();
}

void funcaoBotao1(GFButton& botaoDoEvento) {
  int indiceLocal = indiceLetraGlobal;

  if (indiceLocal < texto.length()) {

    int posicaoLetra = tolower(texto.charAt(indiceLocal)) - 96;
    myDFPlayer.play(posicaoLetra);
    Serial.println(texto.substring(indiceLocal, indiceLocal + 1));
  }
}

void funcaoBotao2(GFButton& botaoDoEvento) {
  int indiceLocal = indiceLetraGlobal + 1;

  if (indiceLocal < texto.length()) {

    int posicaoLetra = tolower(texto.charAt(indiceLocal)) - 96;
    myDFPlayer.play(posicaoLetra);
    Serial.println(texto.substring(indiceLocal, indiceLocal + 1));
  }
}

void funcaoBotao3(GFButton& botaoDoEvento) {
  int indiceLocal = indiceLetraGlobal + 2;

  if (indiceLocal < texto.length()) {

    int posicaoLetra = tolower(texto.charAt(indiceLocal)) - 96;
    myDFPlayer.play(posicaoLetra);
    Serial.println(texto.substring(indiceLocal, indiceLocal + 1));
  }
}

void funcaoBotao4(GFButton& botaoDoEvento) {
  int indiceLocal = indiceLetraGlobal + 3;

  if (indiceLocal < texto.length()) {

    int posicaoLetra = tolower(texto.charAt(indiceLocal)) - 96;
    myDFPlayer.play(posicaoLetra);
    Serial.println(texto.substring(indiceLocal, indiceLocal + 1));
  }
}

void funcaoSensor(GFButton& botaoDoEvento) {
  unsigned long tempoAtual = millis();
  if (tempoAtual - tempoAnteriorSensor > 3500) {
    indiceLetraGlobal += 4;
    tempoAnteriorSensor = millis();
    Serial.println("Avançou");
    if (indiceLetraGlobal >= texto.length()){
      indiceLetraGlobal = 0;
    }
  }
}
