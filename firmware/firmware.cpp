#include <Arduino.h>
#include <Wire.h>                //enable I2C.
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <WiFi.h>
#include <ESPAsyncWebServer.h>

#define SDA_PIN 21  
#define SCL_PIN 22 

static const uint8_t do_address = 100;
static const uint8_t ph_address = 99;
static const char read_command[] = "R";

Adafruit_BME280 bme;

const char* ssid = "Lance2152";
AsyncWebServer server(80);

bool water_pump_on = false;

void startAtlasRead(const uint8_t device_address) {
  Wire.beginTransmission(device_address);
  Wire.write((uint8_t*)read_command, 1);
  Wire.endTransmission();
}

float readAddress(const uint8_t device_address) {
  Wire.requestFrom(device_address, 20, 1);
  byte code = Wire.read();

  switch (code) {
    case 1:
      Serial.println("Success");
      break;

    case 2:
      Serial.println("Failed");
      break;

    case 254:
      Serial.println("Pending");
      break;

    case 255:
      Serial.println("No Data");
      break;
  }

  char device_data[20];

  byte i = 0;
  while (Wire.available()) {
    char in_char = Wire.read();
    device_data[i] = in_char;
    i += 1;
    if (in_char == 0) {
      i = 0;
      break;
    }
  }

  return atof(device_data);
}
 
void setup()                     //hardware initialization.
{
  Serial.begin(115200);           //enable serial port.
  Wire.begin(SDA_PIN, SCL_PIN);

  if (!bme.begin(0x77)) {
    Serial.println("Could not find a valid BME280 sensor!");
    while (1);
  }

  pinMode(4, OUTPUT);

  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/html", "testing");
  });

  server.on("/temp", HTTP_GET, [](AsyncWebServerRequest *request) {
    char buffer[128];
    sprintf(buffer, "{\"temperature\": %f, \"humidity\": %f}", bme.readTemperature(), bme.readHumidity());
    request->send(200, "text/html", buffer);
  });

  server.on("/ph", HTTP_GET, [](AsyncWebServerRequest *request) {
    startAtlasRead(ph_address);
    delay(815);
    float ph = readAddress(ph_address);
    char buffer[128];
    sprintf(buffer, "{\"ph\": %f}", ph);
    request->send(200, "text/html", buffer);
  });

  server.on("/do", HTTP_GET, [](AsyncWebServerRequest *request) {
    startAtlasRead(do_address);
    delay(815);
    float dissolved_oxygen = readAddress(do_address);
    char buffer[128];
    sprintf(buffer, "{\"do\": %f}", dissolved_oxygen);
    request->send(200, "text/html", buffer);
  });

  server.on("/waterpump", HTTP_GET, [](AsyncWebServerRequest *request) {
    bool old_status = water_pump_on;
    if (water_pump_on) {
      digitalWrite(4, LOW);
      water_pump_on = false;
    } else {
      digitalWrite(4, HIGH);
      water_pump_on = true;
    }
    char buffer[128];
    sprintf(buffer, "{\"previous_state\": \"%s\", \"new_state\": \"%s\"}", old_status ? "on" : "off", water_pump_on ? "on" : "off");
    request->send(200, "text/html", buffer);
  });

  server.begin();
}
 
 
void loop() {
}

