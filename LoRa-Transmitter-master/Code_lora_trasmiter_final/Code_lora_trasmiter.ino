#include <SoftwareSerial.h>
#include <Wire.h>

SoftwareSerial loraSerial(10,9); // TX, RX //Portas da logica serial

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
  
  //Prints port Serial
  //Serial.print("velocidade:");
  loraSerial.print(";");
  loraSerial.print(velocidade);
  //Serial.print("bateria:");
  loraSerial.print(";");
  loraSerial.print(bateria);
  //Serial.print("rpm:");
  loraSerial.print(";");
  loraSerial.print(rpm);
  //Serial.print("gasolina_1:");
  loraSerial.print(";");
  loraSerial.print(gasolina_1);
  //Serial.print("gasolina_2:");
  loraSerial.print(";");
  loraSerial.println(gasolina_2);

  delay(3000);

}
