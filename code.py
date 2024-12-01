import streamlit as st

st.title("Display Text/Images using OLED")

code = """
#include <Wire.h>                    // For I2C communication
#include <Adafruit_GFX.h>             // For basic graphics functions
#include <Adafruit_SSD1306.h>         // For OLED display

#define SCREEN_WIDTH 128             // OLED display width
#define SCREEN_HEIGHT 64             // OLED display height
#define OLED_RESET    -1             // Reset pin, set to -1 if not used
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  // Start the serial communication
  Serial.begin(115200);
  
  // Initialize the OLED display
  if (!display.begin(SSD1306_I2C_ADDRESS, OLED_RESET)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);  // Infinite loop if OLED init fails
  }
  display.display();  // Initialize the display with black background
  delay(2000);        // Wait for 2 seconds
  
  // Display text on the screen
  display.clearDisplay();
  display.setTextSize(1);      // Text size
  display.setTextColor(SSD1306_WHITE); // Text color
  display.setCursor(0,0);     // Set cursor to top-left
  display.println(F("Hello, World!"));
  display.display();          // Show the text
}

void loop() {
  // You can add more display functionality here
  // Example: Create an animation or display other data
}
"""

st.code(code, language="c++")


st.title("Controlling an LED using webpage")

code = """
#include <ESP8266WiFi.h>
#include <ESPAsyncWebServer.h>

// Replace with your Wi-Fi credentials
const char* ssid = "Your_SSID";
const char* password = "Your_PASSWORD";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

// Define LED pin
const int ledPin = D2;

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);

  // Set LED pin as output
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // LED is off initially

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to Wi-Fi...");
  }
  Serial.println("Connected to Wi-Fi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Handle root URL
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(200, "text/html", R"rawliteral(
      <!DOCTYPE html>
      <html>
      <head>
        <title>Control LED</title>
        <style>
          button { font-size: 20px; padding: 10px; margin: 10px; }
        </style>
      </head>
      <body>
        <h1>Control LED</h1>
        <button onclick="fetch('/on')">Turn ON</button>
        <button onclick="fetch('/off')">Turn OFF</button>
      </body>
      </html>
    )rawliteral");
  });

  // Handle ON request
  server.on("/on", HTTP_GET, [](AsyncWebServerRequest *request) {
    digitalWrite(ledPin, HIGH); // Turn on LED
    request->send(200, "text/plain", "LED ON");
  });

  // Handle OFF request
  server.on("/off", HTTP_GET, [](AsyncWebServerRequest *request) {
    digitalWrite(ledPin, LOW); // Turn off LED
    request->send(200, "text/plain", "LED OFF");
  });

  // Start server
  server.begin();
}

void loop() {
  // Nothing to do here
}
"""

st.code(code, language="c++")