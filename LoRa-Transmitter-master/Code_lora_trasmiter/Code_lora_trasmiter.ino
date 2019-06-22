#include <SoftwareSerial.h>
#include <Wire.h>

SoftwareSerial loraSerial(8, 9); // TX, RX //Portas da logica serial

float velocidade = 0;
float bateria = 0;
float rpm = 0;
float gasolina_1 = 0;
float gasolina_2 = 0;


void setup() {
  Serial.begin(9600);
  loraSerial.begin(9600);
}

void loop() {

  velocidade = 60;
  bateria = 90;
  rpm = 1700;
  gasolina_1 = 1;
  gasolina_2 = 1;

  //Prints Modulo Lora E32 Series
  loraSerial.print("velocidade");
  loraSerial.println(String(velocidade));
  loraSerial.print("bateria:");
  loraSerial.println(String(bateria));
  loraSerial.print("rpm");
  loraSerial.println(String(rpm));
  loraSerial.print("gasolina_1");
  loraSerial.println(String(gasolina_1));
  loraSerial.print("gasolina_2");
  loraSerial.println(String(gasolina_2));


  //Prints port Serial
  //Serial.print("velocidade:");
  Serial.print(";");
  Serial.print(velocidade);
  //Serial.print("bateria:");
  Serial.print(";");
  Serial.print(bateria);
  //Serial.print("rpm:");
  Serial.print(";");
  Serial.print(rpm);
  //Serial.print("gasolina_1:");
  Serial.print(";");
  Serial.print(gasolina_1);
  //Serial.print("gasolina_2:");
  Serial.print(";");
  Serial.println(gasolina_2);

  delay(3000);

  Serial.print(";");
  Serial.print(velocidade+100);
  //Serial.print("bateria:");
  Serial.print(";");
  Serial.print(bateria+100);
  //Serial.print("rpm:");
  Serial.print(";");
  Serial.print(rpm+100);
  //Serial.print("gasolina_1:");
  Serial.print(";");
  Serial.print(gasolina_1+100);
  //Serial.print("gasolina_2:");
  Serial.print(";");
  Serial.println(gasolina_2+100);

  delay(3000);
}

