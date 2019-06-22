float velocidade = 34;
float bateria = 75;
float rpm = 1335;
float gasolina = 75;

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print("Fox");
  Serial.print(";");
  Serial.print(velocidade);
  Serial.print(";");
  Serial.print(bateria);
  Serial.print(";");
  Serial.print(rpm);
  Serial.print(";");
  Serial.print(gasolina);
  Serial.print(";");
  Serial.print("\n");

  delay(1000);
}
