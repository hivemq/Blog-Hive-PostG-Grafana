#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_SHT31.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Replace with your Wi-Fi credentials
const char* ssid = "Your_SSID";
const char* password = "Your_PASSWORD";

// Replace with your MQTT broker information
const char* mqtt_server = "broker.hivemq.com";
const char* mqtt_topic = "sensor/sht30";

WiFiClient espClient;
PubSubClient client(espClient);
Adafruit_SHT31 sht30 = Adafruit_SHT31();

void setupWiFi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("WemosClient")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setupWiFi();
  client.setServer(mqtt_server, 1883);

  if (!sht30.begin(0x44)) { // 0x44 is the I2C address for the SHT30
    Serial.println("Couldn't find SHT30 sensor!");
    while (1);
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float temperature = sht30.readTemperature();
  float humidity = sht30.readHumidity();

  if (!isnan(temperature) && !isnan(humidity)) {
    char payload[100];
    snprintf(payload, sizeof(payload), "{\"temperature\": %.2f, \"humidity\": %.2f}", temperature, humidity);
    Serial.println(payload);
    client.publish(mqtt_topic, payload);
  } else {
    Serial.println("Failed to read from SHT30 sensor");
  }

  delay(5000); // Send data every 5 seconds
}
