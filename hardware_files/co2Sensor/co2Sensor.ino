#include <WiFi.h>
#include <Wire.h>
#include <WiFiClient.h>
#include <HTTPClient.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

static const uint8_t logo_polkadot[512] = {
  0x00, 0x00, 0x00, 0x3f, 0xc0, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x01, 0xff, 0xf8, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x07, 0xff, 0xfe, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x0f, 0xff, 0xff, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x1f, 0xff, 0xff, 0x80, 0x00, 0x00, 
  0x00, 0x00, 0x1f, 0xff, 0xff, 0x80, 0x00, 0x00, 
  0x00, 0x00, 0x1f, 0xff, 0xff, 0x80, 0x00, 0x00, 
  0x00, 0x00, 0x1f, 0xff, 0xff, 0x80, 0x00, 0x00, 
  0x00, 0x00, 0x1f, 0xff, 0xff, 0x80, 0x00, 0x00, 
  0x00, 0x7c, 0x0f, 0xff, 0xff, 0x03, 0xe0, 0x00, 
  0x01, 0xfe, 0x07, 0xff, 0xfe, 0x07, 0xf8, 0x00, 
  0x03, 0xff, 0x03, 0xff, 0xfc, 0x0f, 0xfc, 0x00, 
  0x07, 0xff, 0x00, 0xff, 0xf0, 0x0f, 0xfe, 0x00, 
  0x0f, 0xff, 0x00, 0x00, 0x00, 0x0f, 0xff, 0x00, 
  0x1f, 0xff, 0x00, 0x00, 0x00, 0x0f, 0xff, 0x80, 
  0x1f, 0xff, 0x00, 0x00, 0x00, 0x0f, 0xff, 0x80, 
  0x3f, 0xff, 0x00, 0x00, 0x00, 0x0f, 0xff, 0xc0, 
  0x3f, 0xff, 0x00, 0x00, 0x00, 0x0f, 0xff, 0xc0, 
  0x7f, 0xff, 0x00, 0x00, 0x00, 0x0f, 0xff, 0xe0, 
  0x7f, 0xfe, 0x00, 0x00, 0x00, 0x07, 0xff, 0xe0, 
  0x7f, 0xfe, 0x00, 0x00, 0x00, 0x07, 0xff, 0xe0, 
  0xff, 0xfe, 0x00, 0x00, 0x00, 0x07, 0xff, 0xf0, 
  0xff, 0xfc, 0x00, 0x00, 0x00, 0x03, 0xff, 0xf0, 
  0xff, 0xf8, 0x00, 0x00, 0x00, 0x01, 0xff, 0xf0, 
  0xff, 0xf8, 0x00, 0x00, 0x00, 0x01, 0xff, 0xf0, 
  0xff, 0xf0, 0x00, 0x00, 0x00, 0x00, 0xff, 0xf0, 
  0xff, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x7f, 0xf0, 
  0x7f, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xe0, 
  0x7f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x1f, 0xe0, 
  0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x80, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x80, 
  0x7f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x1f, 0xe0, 
  0x7f, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xe0, 
  0xff, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x7f, 0xf0, 
  0xff, 0xf0, 0x00, 0x00, 0x00, 0x00, 0xff, 0xf0, 
  0xff, 0xf8, 0x00, 0x00, 0x00, 0x01, 0xff, 0xf0, 
  0xff, 0xf8, 0x00, 0x00, 0x00, 0x01, 0xff, 0xf0, 
  0xff, 0xfc, 0x00, 0x00, 0x00, 0x03, 0xff, 0xf0, 
  0xff, 0xfe, 0x00, 0x00, 0x00, 0x07, 0xff, 0xf0, 
  0x7f, 0xfe, 0x00, 0x00, 0x00, 0x07, 0xff, 0xe0, 
  0x7f, 0xfe, 0x00, 0x00, 0x00, 0x07, 0xff, 0xe0, 
  0x7f, 0xff, 0x00, 0x00, 0x00, 0x0f, 0xff, 0xe0, 
  0x3f, 0xff, 0x00, 0x00, 0x00, 0x0f, 0xff, 0xc0, 
  0x3f, 0xff, 0x00, 0x00, 0x00, 0x0f, 0xff, 0xc0, 
  0x1f, 0xff, 0x00, 0x00, 0x00, 0x0f, 0xff, 0x80, 
  0x1f, 0xff, 0x00, 0x00, 0x00, 0x0f, 0xff, 0x80, 
  0x0f, 0xff, 0x00, 0x00, 0x00, 0x0f, 0xff, 0x00, 
  0x07, 0xff, 0x00, 0xff, 0xf0, 0x0f, 0xfe, 0x00, 
  0x03, 0xff, 0x03, 0xff, 0xfc, 0x0f, 0xfc, 0x00, 
  0x01, 0xfe, 0x07, 0xff, 0xfe, 0x07, 0xf8, 0x00, 
  0x00, 0x7c, 0x0f, 0xff, 0xff, 0x03, 0xe0, 0x00, 
  0x00, 0x00, 0x1f, 0xff, 0xff, 0x80, 0x00, 0x00, 
  0x00, 0x00, 0x1f, 0xff, 0xff, 0x80, 0x00, 0x00, 
  0x00, 0x00, 0x1f, 0xff, 0xff, 0x80, 0x00, 0x00, 
  0x00, 0x00, 0x1f, 0xff, 0xff, 0x80, 0x00, 0x00, 
  0x00, 0x00, 0x1f, 0xff, 0xff, 0x80, 0x00, 0x00, 
  0x00, 0x00, 0x0f, 0xff, 0xff, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x07, 0xff, 0xfe, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x01, 0xff, 0xf8, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x3f, 0xc0, 0x00, 0x00, 0x00, 
  };


const char* ssid = "Milo";
const char* password = "97274340";
String wallet = "5D2fBKHgezt6pKKuXFo8Xse3sT9hZK5PtkJEyacozZJnVXZ3";
String token = "0ce956fc-131b-42d6-a4b1-8e8319e45f84";
String serverName = "http://ec2-54-234-110-184.compute-1.amazonaws.com:8086/data_co/";
String source = "Sensor";
const int sensorPin = 36;
int sensorValue = 0;

WiFiClient wifiClient;

void setup() {
  
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  delay(500);

  Wire.begin(5, 4);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C, false, false)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  } 

    // Conexi??n wifi
  while (WiFi.status() != WL_CONNECTED) {
 
    delay(1000);
    Serial.println("Connecting..");
    
    }

  // Mensaje exito conexi??n
  Serial.println("======================================");
  Serial.print("Conectado a:\t");
  Serial.println(WiFi.SSID()); 
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());
  Serial.println("======================================"); 
  
}


void loop() {
  
  display.clearDisplay();
  display.drawBitmap(64, 0, logo_polkadot, 60, 64, 1);

  sensorValue = analogRead(sensorPin) * 0.7;
  Serial.println(sensorValue);
  
  // Tama??o del texto
  display.setTextSize(2);
  // Color del texto
  display.setTextColor(SSD1306_WHITE);
  // Posici??n del texto
  display.setCursor(10, 4);
  // Escribir texto
  display.println("ppm:");
    // Posici??n del texto
  display.setCursor(10, 26);
  // Escribir texto
  display.println(sensorValue);

  if (int(sensorValue) > 820){
      display.setCursor(2, 48);
      // Escribir texto
      display.println("send!");
  }
    
  if (WiFi.status() == WL_CONNECTED) { 

  HTTPClient http;  
  String serverPath = serverName + "?co2=" + sensorValue + "&origin=" + source + "&wallet_send=" + wallet + "&token=" + token; 

  http.begin(wifiClient, serverPath);                         
  int httpCode = http.GET();                                 
  Serial.println("request OK");

  if (httpCode > 0) { 

    String payload = http.getString();   
    Serial.println(payload);            

    }
  
  http.end();
  
  }      
  
  delay(15000);
    
 
  // Enviar a pantalla
  display.display();
  delay(1000);
}
