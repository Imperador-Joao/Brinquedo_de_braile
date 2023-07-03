#include "Arduino.h"
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"
#include <GFButton.h>
#include <ShiftDisplay.h>


GFButton botao1(A8);
GFButton botao2(A9);
GFButton botao3(A10);
GFButton botao4(A11);

GFButton sensor(A12);

int indiceLetraGlobal = 0;

int potenciometroVolume = A7;
int volume;

int rclk = 12;
int sclk = 11;
int dio = 10;
int indicesDisplay[] = { 3, 2, 1, 0 };

unsigned long tempoAnteriorSensor;

String texto;
DFRobotDFPlayerMini myDFPlayer;
ShiftDisplay display(rclk, sclk, dio, COMMON_ANODE, 4, true, indicesDisplay);



void setup() {
  // put your setup code here, to run once:
  pinMode(potenciometroVolume, INPUT);

  Serial.begin(115200);
  Serial1.begin(9600);


  botao1.setReleaseHandler(funcaoBotao1);
  botao2.setReleaseHandler(funcaoBotao2);
  botao3.setReleaseHandler(funcaoBotao3);
  botao4.setReleaseHandler(funcaoBotao4);

  sensor.setReleaseHandler(funcaoSensor);
  //SoftwareSerial mySoftwareSerial(19, 18); // RX, TX
  //mySoftwareSerial.begin(9600);

  if (!myDFPlayer.begin(Serial1)) {
    Serial.println(F("Nao inicializado:"));
    Serial.println(F("1.Cheque as conexoes do DFPlayer Mini"));
    Serial.println(F("2.Insira um cartao SD"));
  } else {
    Serial.println(F("Inicializado com sucesso:"));
    myDFPlayer.volume(19);
  }
}

void loop() {

  botao1.process();
  botao2.process();
  botao3.process();
  botao4.process();

  sensor.process();

  volume = map(analogRead(potenciometroVolume), 0, 1023, 0, 30);
  myDFPlayer.volume(volume);

  if (Serial.available()) {
    texto = Serial.readStringUntil('\n');
    texto.trim();
    indiceLetraGlobal = 0;
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
    
  }
}
