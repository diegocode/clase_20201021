/*
  Rui Santos
  Complete project details at Complete project details at https://RandomNerdTutorials.com/esp8266-nodemcu-http-get-post-arduino/

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  Modificado diegoCode / 20201021 

*/

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

// usar nombre de la red wifi a la que se conectará la placa
const char* ssid = "user";
// usar password de la red wifi a la que se conectará la placa
const char* password = "password";

//Your Domain name with URL path or IP address with path
String serverName = "http://diegocode.pythonanywhere.com/datain";

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
// Timer set to 10 minutes (600000)
//unsigned long timerDelay = 600000;
// Set timer to 5 seconds (5000)
unsigned long timerDelay = 5000;

void setup() {
  Serial.begin(115200); 

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
}

int vin;
String vin_str;
const String num_sensor = "85";

float val_temp;

void loop() {
  //Send an HTTP POST request every 10 minutes
  if ((millis() - lastTime) > timerDelay) {      
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;

      // Leo entrada analógica
      // y convierto 3.3V --> 70°C
      vin=analogRead(A0);  //Read Analog value of LDR
      
      val_temp = vin / 1023.0 * 70.0; 
      
      vin_str= String(val_temp);

      //Serial.printf("ADC=%4d Temp=%6.2f\n", vin, val_temp);

      // armo request
      // tempe=
      // hume=
      // snum=
      String serverPath = serverName + "?tempe=" + vin_str + "&hume=77.3" + "&snum=" + num_sensor;
      
      // muestra pedido
      Serial.println(serverPath);
      
      // Your Domain name with URL path or IP address with path
      http.begin(serverPath.c_str());
      
      // Send HTTP GET request
      int httpResponseCode = http.GET();
      
      if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        Serial.println(payload);
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}

