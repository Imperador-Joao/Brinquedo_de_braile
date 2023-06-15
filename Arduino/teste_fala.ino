#include <ShiftDisplay.h>
#include <string.h>
#include <Talkie.h>
#include "Vocab_US_Acorn.h"


int rclk = 12;
int sclk = 11;
int dio = 10;
int indexes[] = { 3, 2, 1, 0 };

int terra = A5;
int campainha = 6;

int indiceRolagem = 0;
bool terminouRolar = true;

int indiceFala = 0;
bool terminouFalar = true;

unsigned long instanteAnterior = 0;

ShiftDisplay display(rclk, sclk, dio, COMMON_ANODE, 4, true, indexes);
Talkie voz;

String texto;

void somDaLetra(char letra) {

  switch (letra) {

    case 'a':
      voz.say(spa_A); break;
    case 'b':
      voz.say(spa_B); break;
    case 'c':
      voz.say(spa_C); break;
    case 'd':
      voz.say(spa_D); break;
    case 'e':
      voz.say(spa_E); break;
    case 'f':
      voz.say(spa_F); break;
    case 'g':
      voz.say(spa_G); break;
    case 'h':
      voz.say(spa_H); break;
    case 'i':
      voz.say(spa_I); break;
    case 'j':
      voz.say(spa_J); break;
    case 'k':
      voz.say(spa_K); break;
    case 'l':
      voz.say(spa_L); break;
    case 'm':
      voz.say(spa_M); break;
    case 'n':
      voz.say(spa_N); break;
    case 'o':
      voz.say(spa_O); break;
    case 'p':
      voz.say(spa_P); break;
    case 'q':
      voz.say(spa_Q); break;
    case 'r':
      voz.say(spa_R); break;
    case 's':
      voz.say(spa_S); break;
    case 't':
      voz.say(spa_T); break;
    case 'u':
      voz.say(spa_U); break;
    case 'v':
      voz.say(spa_V); break;
    case 'w':
      voz.say(spa_W); break;
    case 'x':
      voz.say(spa_X); break;
    case 'y':
      voz.say(spa_Y); break;
    case 'z':
      voz.say(spa_Z); break;
    default:
      Serial.println("letra inválida");
  }

}

void setup() {
  // put your setup code here, to run once:

  pinMode(terra, OUTPUT);
  digitalWrite(terra, HIGH);

  pinMode(campainha, OUTPUT);

  Serial.begin(9600);

}



void loop() {
  // put your main code here, to run repeatedly:



  unsigned long instanteAtual = millis();
  int comprimentoTexto = texto.length();

  if (Serial.available() && terminouRolar && terminouFalar) {
    texto = Serial.readStringUntil('\n');
    texto.trim();

    Serial.println(texto);

    indiceFala = 0;
    indiceRolagem = 0;

    terminouRolar = false;
    terminouFalar = false;
    display.set(texto);
  }




  if (comprimentoTexto == 0) {
    terminouRolar = true;
    terminouFalar = true;
  }

  else if (instanteAtual - instanteAnterior >= 1000) {


    if (indiceFala < texto.length()) {
      somDaLetra(texto.charAt(indiceFala));
      indiceFala++;
    }
    else {
      terminouFalar = true;
    }



    if (indiceRolagem + 4 < texto.length()) {
      indiceRolagem += 4;

      String subtexto = texto.substring(indiceRolagem);
      display.set(subtexto);

    }
    else {
      display.set("");
      terminouRolar = true;

    }
    instanteAnterior = millis();
  }


  display.update();
}
