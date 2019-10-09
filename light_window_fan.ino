#include <ESP8266WiFi.h>
#include <PubSubClient.h> 

#define BUILTIN_LED 2

// Update these with values suitable for your network.
const char* ssid = "WIFI-LIS";                   // Modificar
//const char* password = "SSID_PASSWORD";           // Modificar
const char* mqtt_server = "192.168.192.7";            // Modificar

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.disconnect();
  delay(100);
  WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    Serial.print(WiFi.status());
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  String command;
  for (int i = 0; i < length; i++) {
    command += (char)payload[i];
  }
  Serial.print(command);  
  Serial.println(); 
  if (command == "ON" || command == "OPEN") {
    // Turn On the lamp  
    digitalWrite(BUILTIN_LED, LOW);
  }
  else {
    // Turn Off the lamp
    digitalWrite(BUILTIN_LED, HIGH);
  }   
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // ... and resubscribe
      client.subscribe("hospital/room/light");
      client.subscribe("hospital/room/window");
      client.subscribe("hospital/room/fan");
    } 
    else {
      Serial.print("failed connection, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}