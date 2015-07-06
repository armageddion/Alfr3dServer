#include <Servo.h> 

String inStr = "";  // variable to hold data received from pi
boolean inSrt_complete=false;
String content = "";
char character;

// Arduino Pins
int ledPin = 13;        // LED Pin

int pump1Pin = 3;       // Pump pin
int pump2Pin = 2;       // Pump pin
//int HygroPinA0 = 2;     // Analog input from Hygrometer - NOT WORKING
//int HygroPinD0 = 3;     // Digital input from Hygrometer

// RF1
boolean RF1 = false;
int RF1_pin1 = 12;      // RF1 control pin
int RF1_pin2 = 9;       // RF1 control pin

// RF2
boolean RF2 = false;
int RF2_pin1 = 11;      // RF2 control pin
int RF2_pin2 = 8;       // RF2 control pin

// RF3
boolean RF3 = false;
int RF3_pin1 = 10;      // RF3 control pin
int RF3_pin2 = 7;       // RF3 control pin

int clicks = 0;         // how many dimmer clicks do we have (MAX 21-24)
int brightness = 0;     // 0 - 100: {0, 20, 40, 60, 80, 100}
int dimmer_pin1 = 5;    // dimmer ON
//int dimmer_pin2 = 3;        // dimmer UP
//int dimmer_pin3 = 4;        // dimmer MIDDLE
//int dimmer_pin4 = 5;        // dimmer DOWN
int dimmer_pin5 = 6;    // dimmer OFF

// int analVal = 0;        // Variable to hold actual analog value received from Hygrometer
// int digVal = 0;         // Variable to hold actual digita value received from Hygrometer
// int soilHumidityD = 0;  // Variable to hold boolean (HIGH|LOW) moisture value
// int soilHumidityA = 0;  // Variable to hold analog (0-1024) moisture value

void setup() {
  Serial.begin(9600);      // opens serial port, sets data rate to 9600 bps
  pinMode(ledPin, OUTPUT); 

  pinMode(pump1Pin, OUTPUT);  
  pinMode(pump2Pin, OUTPUT);  

  pinMode(RF1_pin1, OUTPUT);
  pinMode(RF1_pin2, OUTPUT);

  pinMode(RF2_pin1, OUTPUT);
  pinMode(RF2_pin2, OUTPUT);  

  pinMode(RF3_pin1, OUTPUT);
  pinMode(RF3_pin2, OUTPUT);

  pinMode(dimmer_pin1, OUTPUT);
  pinMode(dimmer_pin5, OUTPUT);

  //pinMode(HygroPinA0, INPUT); 
  //pinMode(HygroPinD0, INPUT); 
}

void loop() {
  if(inStr.equals("Blink")){
    digitalWrite(ledPin,HIGH);
    delay(1000);
    digitalWrite(ledPin,LOW);
    delay(1000);
    digitalWrite(ledPin,HIGH);
    delay(1000);
    digitalWrite(ledPin,HIGH);
    delay(1000);     
    digitalWrite(ledPin,LOW);
    delay(1000);     
    Serial.println("Blinked");
  }
  else if (inStr.equals("Pump1On")){
    digitalWrite(pump1Pin,HIGH);
    Serial.println("Pump1 On");
  }
  else if (inStr.equals("Pump1Off")){
    digitalWrite(pump1Pin,LOW);        
    Serial.println("Pump1 Off");
  }    
  else if (inStr.equals("Pump2On")){
    digitalWrite(pump2Pin,HIGH);
    Serial.println("Pump2 On");
  }
  else if (inStr.equals("Pump2Off")){
    digitalWrite(pump2Pin,LOW);        
    Serial.println("Pump2 Off");
  }      
  else if (inStr.equals("RF1ON")){
    digitalWrite(RF1_pin1,HIGH);
    delay(1500);
    digitalWrite(RF1_pin1,LOW);
    Serial.println("RF1 On");
  }
  else if (inStr.equals("RF1OFF")){
    digitalWrite(RF1_pin2,HIGH);
    delay(1500);
    digitalWrite(RF1_pin2,LOW);
    Serial.println("RF1 Off");    
  }  
  else if (inStr.equals("RF2ON")){
    digitalWrite(RF2_pin1,HIGH);
    delay(1500);
    digitalWrite(RF2_pin1,LOW);
    Serial.println("RF2 On");    
  }  
  else if (inStr.equals("RF2OFF")){
    digitalWrite(RF2_pin2,HIGH);
    delay(1500);
    digitalWrite(RF2_pin2,LOW);
    Serial.println("RF2 Off");    
  }  
  else if (inStr.equals("RF3ON")){
    digitalWrite(RF3_pin1,HIGH);
    delay(1500);
    digitalWrite(RF3_pin1,LOW);
    Serial.println("RF3 On");    
  }  
  else if (inStr.equals("RF3OFF")){
    digitalWrite(RF3_pin2,HIGH);
    delay(1500);
    digitalWrite(RF3_pin2,LOW);
    Serial.println("RF3 Off");    
  }
  else if (inStr.equals("LightsON")){
    digitalWrite(dimmer_pin1,HIGH);
    delay(3000);
    digitalWrite(dimmer_pin1,LOW);
    Serial.println("Lights On");    
  }  
  else if (inStr.equals("LightsOFF")){
    digitalWrite(dimmer_pin5,HIGH);
    delay(3000);
    digitalWrite(dimmer_pin5,LOW);
    Serial.println("Lights Off");        
  }      
  // else if (inStr.equals("Read Humidity A")){
  //   analVal = analogRead(A2);
  //   delay(1000);     
  //   Serial.println("Analog Read = "+analVal);
  // }
  // else if (inStr.equals("Read Humidity D")){
  //   digVal = digitalRead(HygroPinD0);
  //   if (digVal == HIGH){
  //         soilHumidityD = LOW;
  //         Serial.println("Digital Read is HIGH");
  //         Serial.println("Soil Humidity is LOW");
  //   }
  //   else{
  //         soilHumidityD = HIGH;      
  //         Serial.println("Digital Read is LOW");
  //         Serial.println("Soil Humidity is HIGH");
  //   }
  // }
  else{
    Serial.println("unknown method call: "+inStr);
  }

  inStr=""; 
}

void serialEvent(){
  while(Serial.available()>0) {
    character = Serial.read();
    if(character=='\n'){
      inStr=content;
      Serial.println("inStr = "+inStr);
      content="";
      return;
    }
    else{
      content.concat(character);
    }
  }

  if (content != "") {
    //Serial.println(content);
  }
}





