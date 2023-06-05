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

// Servos
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;
Servo servo7;
Servo servo8;

struct servoPos
{
  int[3] posDes    //Define a posicao do servo
  int braileTag    //Variavel para facilitar a correlacao de movimentos dos servos (1,2,3 ou 4)
                   //Ex: TagBraile[0] -> 1o caracter em Braile, sera possivel garantir que apenas servo 1 e servo 2 atuem para o braile 1.
}

LinkedList<servoPos> listaDeServos; //Dois servos para cada caracter Braile -> Total de 8 servos

void setup()
{
  // Inicializando a comunicacao serial.
  Serial.begin(9600);

  // Parametros
  // [0] = pino ; [1] = comprimento minimo do pulso PWM (corresponde a 0 graus); [2] = comprimento maximo do pulso PWM (corresponde a 180 graus)
  servo1.attach(4, 1000, 2000);
  servo2.attach(5, 1000, 2000);

  // Movimenta servo 1.
  botao1.setPressHandler(moverServo);
  // Movimenta servo 2.
  botao2.setPressHandler(moverServo);
}

void movimentaServo(int posicaoDesejada, int indiceServo)
{
  switch (posicaoDesejada)
  {
   //Angulo no servo = 2 * Angulo no Octogno
   //Passo do servo = 180/8 = 22.5
   
    case 000: // Posicao 1 -> Braile - - -
      servo.write(23) //Servo:22.5 = Octogono:45
      Serial.println("000");
      break; //Quebra o switch case e reverifica os casos

    case 001: // Posicao 2 -> Braile - - *
      servo.write(45) //Servo:45 = Octogono:90
      Serial.println("001");
      break;

    case 010: // Posicao 3 -> Braile - * -
      servo.write(68) //Servo:67.5 = Octogono:135
      Serial.println("010");
      break;

    case 011: // Posicao 4 -> Braile - * *
      servo.write(90) //Servo:90 = Octogono:180
      Serial.println("011");
      break;

    case 100: // Posicao 5 -> Braile * - -
      servo.write(113) //Servo:112.5 = Octogono:225
      Serial.println("100");
      break;

    case 101: // Posicao 6 -> Braile * - *
      servo.write(135) //Servo:135 = Octogono:275
      Serial.println("101");
      break;

    case 110: // Posicao 7 -> Braile * * -
      servo.write(158) //Servo:157.5 = Octogono:315
      Serial.println("110");
      break;

    case 111: // Posicao 8 -> Braile * * *
      servo.write(180) //Servo:180 = Octogono:360
      Serial.println("111");
      break;
  }
}

void loop()
{

  botao1.process();
  botao2.process();
  botao3.process();

  if (Serial.available() > 0) 
  {
    String texto = Serial.readStringUntil('\n');
    texto.trim();
    
    //Codificao Braile -> 001001 -> _ _ * _ _ *
    
    //Primeiro Exemplo de Serial recebido: 1001001 -> O primeiro digito informa qual dos caracter braile do mecanismo deve representar, os seguintes 6 digitos as duas colunas que devem ser combinadas
    //Segundo Exemplo de Serial recebido: 3011101 -> Informação para o 3o caracter Braile -> _ * * * _ *
    //Terceiro Exemplo de Serial recebido: 001001,001001,011101,001001 -> Informação para o 3o caracter Braile -> _ * * * _ *

    /*if (texto.startsWith("Braile")) 
    {
    }*/
}
