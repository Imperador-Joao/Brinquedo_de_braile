#include "Arduino.h"
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"
#include <GFButton.h>


GFButton botao1(A8);
GFButton botao2(A9);
GFButton botao3(A10);
GFButton botao4(A11);

int indiceLetraGlobal = 0;

int potenciometroVolume = A7;
int volume;

String texto;
DFRobotDFPlayerMini myDFPlayer;





void setup() {
  // put your setup code here, to run once:
  pinMode(potenciometroVolume,INPUT);

  Serial.begin(115200);
  Serial1.begin(9600);


  botao1.setReleaseHandler(funcaoBotao1);
  botao2.setReleaseHandler(funcaoBotao2);
  botao3.setReleaseHandler(funcaoBotao3);
  botao4.setReleaseHandler(funcaoBotao4);
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

  volume = map(analogRead(potenciometroVolume),0,1023,0,30);
  myDFPlayer.volume(volume);

  if (Serial.available()) {
    texto = Serial.readStringUntil('\n');
    texto.trim();
    int tamanhoTexto = texto.length();
    }
    
  
}

void funcaoBotao1(GFButton& botaoDoEvento) {
  int indiceLocal = indiceLetraGlobal;

  int posicaoLetra = tolower(texto.charAt(indiceLocal)) - 96;
  myDFPlayer.play(posicaoLetra);
  Serial.println(texto.substring(indiceLocal,indiceLocal+1));

}

void funcaoBotao2(GFButton& botaoDoEvento) {
  int indiceLocal = indiceLetraGlobal + 1;

  int posicaoLetra = tolower(texto.charAt(indiceLocal)) - 96;
  myDFPlayer.play(posicaoLetra);
  Serial.println(texto.substring(indiceLocal,indiceLocal+1));
}

void funcaoBotao3(GFButton& botaoDoEvento) {
  int indiceLocal = indiceLetraGlobal + 2;

  int posicaoLetra = tolower(texto.charAt(indiceLocal)) - 96;

  myDFPlayer.play(posicaoLetra);
  Serial.println(texto.substring(indiceLocal,indiceLocal+1));
}

void funcaoBotao4(GFButton& botaoDoEvento) {
  int indiceLocal = indiceLetraGlobal + 3;

  int posicaoLetra = tolower(texto.charAt(indiceLocal)) - 96;
  myDFPlayer.play(posicaoLetra);

  Serial.println(texto.substring(indiceLocal,indiceLocal+1));
}
