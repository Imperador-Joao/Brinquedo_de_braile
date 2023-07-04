//ENG1419_PROJETO_FINAL -> Brinquedo Braile

//Premissa inicial
//montagem de dois servos + programa em Arduino que recebe código braile pela serial e gira servos de acordo

#include <Servo.h>
#include <GFButton.h>
#include <LinkedList.h>

// Botoes
GFButton botao1(A1);
//GFButton botao2(A2);
//GFButton botao3(A3);

struct servoPos
{
  Servo servoVar;
  String posDes;  //Define a posicao do servo
  int posAtual;   //Variavel para acompanhar a posicao dos servos (1,2,3...8)
  //Ex: TagBraile[0] -> 1o caracter em Braile, sera possivel garantir que apenas servo 1 e servo 2 atuem para o braile 1.
};

struct sorteioPalavras
{
  String palavra;
  String braile;
};

servoPos servoPos1;
servoPos servoPos2;
servoPos servoPos3;
servoPos servoPos4;
servoPos servoPos5;
servoPos servoPos6;
servoPos servoPos7;
servoPos servoPos8;

servoPos listaDeServos[] = {servoPos1, servoPos2, servoPos3, servoPos4, servoPos5, servoPos6, servoPos7, servoPos8};
//20 palavras
sorteioPalavras *listaDeSorteios; /*= 
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
int braileTag = 0;  //Variavel para facilitar a correlacao de movimentos dos servos (1,2,3 ou 4)
int braileStart = 0; //Referencial do começo do serial para substring.
int i = 0;
int saveRng = 0;

unsigned long instanteAnterior = 0;

//the time we give the sensor to calibrate (10-60 secs according to the datasheet)
int calibrationTime = 30;        

//the time when the sensor outputs a low impulse
long unsigned int lowIn;         

//the amount of milliseconds the sensor has to be low 
//before we assume all motion has stopped
long unsigned int pause = 5000;  

boolean lockLow = true;
boolean takeLowTime;  

int pirPin = 3;    //the digital pin connected to the PIR sensor's output
int ledPin = 13;

bool eLista = false;
bool eFoto = false;

int posicaoLista = 0;
int qtd_palavras = 0;

void setup() 
{
  // Inicializando a comunicacao serial.
  Serial.begin(9600);
  Serial1.begin(115200);

  randomSeed(analogRead(A0)); // Inicializa elemento aleatório
  botao1.setReleaseHandler(sorteia);
  // Parametros
  // [0] = pino ; [1] = comprimento minimo do pulso PWM (corresponde a 0 graus); [2] = comprimento maximo do pulso PWM (corresponde a 180 graus)
  for (i = 0; i < 8 ; i++) //Inicializa todos os 8 servos
  {
     listaDeServos[i].servoVar.attach(4+i);
     Serial.println(i);
  }
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(pirPin, LOW);
  Serial.print("calibrating sensor ");
}

int binToDec(String binario)
{
  int decimal = 0;

  for (int i = 0; i < binario.length(); i++)
  {
    char digito = binario.charAt(i);
    if (digito == '0')
    {
      decimal = decimal * 2 + 0;
    }
    else if (digito == '1')
    {
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
  //listaDeServoPos[indiceServo].posAtual = posicao;
  int posicaoGraus = 0;
   if (indiceServo%2==0)
  {
     posicaoGraus = 180 - (valor * 25.714);
  }
  else
  {
    posicaoGraus = (valor * 25.714);
  }
  listaDeServos[indiceServo].servoVar.write(posicaoGraus);
  listaDeServos[indiceServo].posAtual = posicaoGraus;
  Serial.print("Angulo em graus: ");
  Serial.println(posicaoGraus);
}

void sorteia(GFButton &botao1)
{
  int randomNumber = random(19);
  //Serial.println(listaDeSorteios[randomNumber].palavra);
  String message = "Braile " + listaDeSorteios[randomNumber].braile;
  Serial.println(message);
}



void leituraDeComando(String texto)
{
  braileStart = 7;  //Indice inicial da sequencia Braile
  braileTag = 1;    //braileTag representa o par de motores que compõe o caracter Braile
  int indiceServo1 = 0;
  int indiceServo2 = 0;
  int quantidadeDeLoops = (texto.length()-7)/6;
  Serial.println(quantidadeDeLoops);
  for (i = 0; i < quantidadeDeLoops ; i++)
  { 
    //&& (millis() - instanteAnterior) > 5000)                                    
    //Através das funcoes abaixo é possível correlacionar o indice da lista de servos com a braileTag
    indiceServo1 = (2*(braileTag - 1)); // 2*(1-1) = 0; 2*(2-1) = 2; 2*(3-1) = 4; 2*(4-1) = 6
    indiceServo2 = ((2*braileTag) - 1); // (2*1)-1 = 1; (2*2)-1 = 3; (2*3)-1 = 5; (2*4)-1 = 7
    listaDeServos[indiceServo1].posDes = texto.substring(braileStart, braileStart + 3);
    listaDeServos[indiceServo2].posDes = texto.substring(braileStart + 3, braileStart + 6);

    Serial.println("Enviando binario");
    Serial.print("Servo 1: ");
    Serial.print(listaDeServos[indiceServo1].posDes);
    Serial.print(",Servo 2 :");
    Serial.println(listaDeServos[indiceServo2].posDes);

    movimentaServo(indiceServo1);     
    movimentaServo(indiceServo2);                   
      
    if (texto.charAt(braileStart + 6) == ',')                   //Exemplo: chegou no caracter 8 -> braileTag = 2
    { 
      Serial.println(texto.charAt(braileStart+6));
      braileStart = braileStart + (6+1);                   // Captura o digito logo após a virgula. Exemplo: Braile 001001,001001 CAPTUROU O '0'
      if (braileTag == 4)
      {
        //sensorDeMovimento();
        //instanteAnterior = millis();
        braileTag = 1;
        delay(5000);
      }
      else
      {
        braileTag++;
      }
    }
  }
}

void loop() 
{
  botao1.process();
  if (Serial1.available() > 0)
  { 
    String texto = Serial1.readStringUntil('\n');
    texto.trim();

    //Codificao Braile -> 1 = * e 0 = -
    Serial.println("HELLO TEXTO");
    Serial.println(texto);
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
      String palavra = texto.substring(1,indexVirgula-1);
      leituraDeComando(texto);
      eFoto = false;
    }

    if (eLista)
    {
      if (posicaoLista < qtd_palavras)
      {
        int indexVirgula = texto.indexOf(",");
        listaDeSorteios[posicaoLista].palavra = texto.substring(1,indexVirgula-1);
        texto = texto.substring(indexVirgula);
        listaDeSorteios[posicaoLista].braile = texto.substring(2,texto.indexOf("',"));
        posicaoLista++;
      }
      
      else
      {
        eLista = false;
        posicaoLista = 0;
      }
    }
   
    if (texto.startsWith("foto")) eFoto = true;
    
    if (texto.startsWith("lista"))
    {
      qtd_palavras = texto.substring(6,7).toInt();
      listaDeSorteios = (sorteioPalavras*)malloc(sizeof(sorteioPalavras)*qtd_palavras);
      eLista = true;
    }
    
    /*if (texto.startsWith("start"))
    {
      Serial.println("startando");
      movimentaServo(0);
    }*/
  }
}
