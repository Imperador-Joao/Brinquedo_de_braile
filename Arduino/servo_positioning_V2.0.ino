//ENG1419_PROJETO_FINAL -> Brinquedo Braile

//Premissa inicial
//montagem de dois servos + programa em Arduino que recebe código braile pela serial e gira servos de acordo

#include <Servo.h>
#include <GFButton.h>
#include <LinkedList.h>

// Botoes
GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);

struct servoPos
{
  Servo servoVar;
  String posDes;  //Define a posicao do servo
  int posAtual;   //Variavel para acompanhar a posicao dos servos (1,2,3...8)
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

servoPos listaDeServos[] = {servoPos1, servoPos2, servoPos3, servoPos4, servoPos5, servoPos6, servoPos7, servoPos8};

int braileTag = 0;  //Variavel para facilitar a correlacao de movimentos dos servos (1,2,3 ou 4)
int braileStart = 0; //Referencial do começo do serial para substring.
int i = 0;

unsigned long instanteAnterior = 0;

void setup() {
  // Inicializando a comunicacao serial.
  Serial.begin(9600);

  // Parametros
  // [0] = pino ; [1] = comprimento minimo do pulso PWM (corresponde a 0 graus); [2] = comprimento maximo do pulso PWM (corresponde a 180 graus)
  for (i = 0; i < 8 ; i++) //Inicializa todos os 8 servos
  {
     listaDeServos[i].servoVar.attach(4+i);
  }
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
  int posicaoGraus = valor * 25.714;

  listaDeServos[indiceServo].servoVar.write(posicaoGraus);
  listaDeServos[indiceServo].posAtual = posicaoGraus;
  Serial.print("Angulo em graus: ");
  Serial.println(posicaoGraus);
}

void loop() {

  if (Serial.available() > 0)
  {
    String texto = Serial.readStringUntil('\n');
    texto.trim();

    //Codificao Braile -> 1 = * e 0 = -
    
    //Primeiro Exemplo de Serial recebido: 1001001 -> O primeiro digito informa qual dos caracter braile do mecanismo deve representar, os seguintes 6 digitos as duas colunas que devem ser combinadas
    //Segundo Exemplo de Serial recebido: 3011101 -> Informação para o 3o caracter Braile -> _ * * * _ *

    if (texto.startsWith("Braile") && ((millis() - instanteAnterior) > 5000))
    {
      braileStart = 7;  //Indice inicial da sequencia Braile
      braileTag = 1;    //braileTag representa o par de motores que compõe o caracter Braile
      
      for (i = 0; i < texto.length() ; i++)
      {
        
        listaDeServos[2*(braileTag - 1)].posDes = texto.substring(braileStart, braileStart + 3);
        listaDeServos[(2*braileTag) - 1)].posDes = texto.substring(braileStart + 3, braileStart + 6);

        Serial.println("Enviando binario");
        Serial.print("Servo 1:");
        Serial.print(listaDeServos[2*(braileTag - 1)].posDes);
        Serial.print(",Servo 2:");
        Serial.println(listaDeServos[(2*braileTag) - 1)].posDes);
                                               
                                               //Através das funcoes abaixo é possível correlacionar o indice da lista de servos com a braileTag
        movimentaServo(2*(braileTag - 1));     // 2*(1-1) = 0; 2*(2-1) = 2; 2*(3-1) = 4; 2*(4-1) = 6
        movimentaServo((2*braileTag) - 1));    // (2*1)-1 = 1; (2*2)-1 = 3; (2*3)-1 = 5; (2*4)-1 = 7
        
        if (texto.charAt(i) == ',')                   //Exemplo: chegou no caracter 8 -> braileTag = 2
        {
          braileStart = i+1;                   // Captura o digito logo após a virgula. Exemplo: Braile 001001,001001 CAPTUROU O '0'
          if (braileTag == 4)
          {
            braileTag = 1;
            instanteAnterior = millis();
          }
          else
          {
            braileTag++;
          }
        }
      }
      
    }
    /*if (texto.startsWith("start"))
    {
      Serial.println("startando");
      movimentaServo(0);
    }*/
  }
}
