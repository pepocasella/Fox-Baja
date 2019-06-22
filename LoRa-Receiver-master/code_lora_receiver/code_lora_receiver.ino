#include <SoftwareSerial.h>
 
SoftwareSerial loraSerial(8, 9); // TX, RX - referencial ao lora
 
void setup() {
  Serial.begin(9600);
  loraSerial.begin(9600);  
}
 
void loop() { 
    if(loraSerial.available() > 1){
    String input = loraSerial.readString();
    Serial.println(input);  
  }
  delay(20);
}
