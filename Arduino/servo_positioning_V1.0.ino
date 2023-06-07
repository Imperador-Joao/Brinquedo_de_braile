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

/* Servos
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;
Servo servo7;
Servo servo8;
*/
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

servoPos listaDeServos[] = {servoPos1,servoPos2,servoPos3,servoPos4,servoPos5,servoPos6,servoPos7,servoPos8};

int braileTag = 0;  //Variavel para facilitar a correlacao de movimentos dos servos (1,2,3 ou 4)

void setup() {
  // Inicializando a comunicacao serial.
  Serial.begin(9600);

  // Parametros
  // [0] = pino ; [1] = comprimento minimo do pulso PWM (corresponde a 0 graus); [2] = comprimento maximo do pulso PWM (corresponde a 180 graus)
  listaDeServos[0].servoVar.attach(4);
  //listaDeServos.add(1).servo.attach(5, 1000, 2000);
  //String data = "111"; //8
  //Serial.print(binStringToInt(data));
  // Movimenta servo 1.
  //botao1.setPressHandler(moverServo);
  // Movimenta servo 2.
  //botao2.setPressHandler(moverServo);
  binToDec("100");
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
    else if(digito == '1')
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

  /*botao1.process();
  botao2.process();
  botao3.process();
  */
  if (Serial.available() > 0) 
  {
    String texto = Serial.readStringUntil('\n');
    texto.trim();

    //Codificao Braile -> 1 = * e 0 = -

    //Primeiro Exemplo de Serial recebido: 1001001 -> O primeiro digito informa qual dos caracter braile do mecanismo deve representar, os seguintes 6 digitos as duas colunas que devem ser combinadas
    //Segundo Exemplo de Serial recebido: 3011101 -> Informação para o 3o caracter Braile -> _ * * * _ *

    if (texto.startsWith("1")) 
    {
      braileTag = 1;
      //Primeiro digito representa qual dos braile. A sequencia sempre começara com o 1 Braile

      //servoEscolhido2 = listaDeServos.get(2*braileTag);

      listaDeServos[braileTag-1].posDes = texto.substring(1, 4);
      //servoEscolhido2.posDes = texto.substring(4, 7);

      //7 virgula, 8 -> braileTag = 2
      Serial.println("enviando binario");
      Serial.println(listaDeServos[braileTag-1].posDes);
    }
    if (texto.startsWith("start")) 
    {
      Serial.println("startando");
      movimentaServo(0);
    }
  }
}

