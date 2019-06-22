//Woon Jun Shen
//UM402 (433 MHz UART)
#include <SoftwareSerial.h>

SoftwareSerial loraSerial(8,9); //TX, RX
// gnd SET_A and SET_B for Normal Mode (Send and Receive)

void setup() {
  Serial.begin(9600);
  loraSerial.begin(9600);
}

void loop() {
  
  
  if(Serial.available() > 0){//Read from serial monitor and send over UM402
    String input = Serial.readString();
    Serial.println(input);    
  }
 
  if(loraSerial.available() > 1){//Read from UM402 and send to serial monitor
    String input = loraSerial.readString();
    Serial.println(input);    
  }
  delay(50);
}
