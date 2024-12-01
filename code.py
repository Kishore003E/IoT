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

st.title("Controlling an LED")

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

st.title("fire acci")

code = """
#include <SoftwareSerial.h>

// Pins for MQ135 and LM35
const int mq135Pin = A0; // Analog pin for MQ135
const int lm35Pin = A0;  // Analog pin for LM35

// GSM module communication
SoftwareSerial gsm(D2, D1); // RX, TX

// Threshold values
const int gasThreshold = 300;     // Adjust based on testing
const float tempThreshold = 50.0; // Threshold in Celsius

void setup() {
  // Initialize Serial Monitors
  Serial.begin(115200);
  gsm.begin(9600);

  // Initialize sensors
  pinMode(mq135Pin, INPUT);
  pinMode(lm35Pin, INPUT);

  // GSM setup
  Serial.println("Initializing GSM...");
  delay(1000);
  gsm.println("AT"); // Check communication
  delay(1000);
  gsm.println("AT+CMGF=1"); // Set SMS mode to text
  delay(1000);
}

void loop() {
  // Read sensors
  int gasValue = analogRead(mq135Pin);
  int tempValue = analogRead(lm35Pin);

  // Convert LM35 output to temperature
  float temperature = (tempValue / 1023.0) * 3.3 * 100.0;

  // Debugging: Print values to Serial Monitor
  Serial.print("Gas Value: ");
  Serial.println(gasValue);
  Serial.print("Temperature: ");
  Serial.println(temperature);

  // Fire condition detection
  if (gasValue > gasThreshold || temperature > tempThreshold) {
    sendAlert(gasValue, temperature);
  }

  delay(5000); // Wait before next reading
}

void sendAlert(int gasValue, float temperature) {
  String message = "FIRE ALERT! Gas: " + String(gasValue) + ", Temp: " + String(temperature) + "C";
  Serial.println("Sending SMS: " + message);

  gsm.println("AT+CMGS=\"+1234567890\""); // Replace with your number
  delay(1000);
  gsm.print(message);
  gsm.write(26); // Send Ctrl+Z to send the SMS
  delay(5000);
}
"""
st.code(code, language="c++")

st.title("GPS")
code = """#include <TinyGPS++.h>
#include <SoftwareSerial.h>

// Create GPS object
TinyGPSPlus gps;

// Define pins for Software Serial
SoftwareSerial gpsSerial(D1, D2); // RX, TX

void setup() {
  Serial.begin(9600);        // Initialize Serial Monitor
  gpsSerial.begin(9600);     // Initialize GPS module communication
  Serial.println("GPS Tracker Starting...");
}

void loop() {
  // Process GPS data
  while (gpsSerial.available() > 0) {
    if (gps.encode(gpsSerial.read())) {
      displayGPSData();
    }
  }
}

// Function to display GPS data
void displayGPSData() {
  if (gps.location.isUpdated()) {
    Serial.print("Latitude: ");
    Serial.println(gps.location.lat(), 6); // 6 decimal places
    Serial.print("Longitude: ");
    Serial.println(gps.location.lng(), 6); // 6 decimal places
  } else {
    Serial.println("Waiting for GPS signal...");
  }
}"""

st.code(code, language="c++")

st.title("Gyro in attiny 85")
code = """#include <Wire.h>
#include <SoftwareSerial.h>
#include <MPU6050.h>

MPU6050 mpu;
SoftwareSerial bluetooth(3, 4); // RX, TX

void setup() {
  // Initialize I2C communication
  Wire.begin();
  
  // Initialize Bluetooth communication
  bluetooth.begin(9600);
  bluetooth.println("Initializing...");

  // Initialize MPU6050
  if (!mpu.begin()) {
    bluetooth.println("MPU6050 not detected!");
    while (1); // Halt if MPU6050 is not connected
  }
  mpu.calcOffsets(); // Calculate offsets for accuracy
  bluetooth.println("MPU6050 Initialized.");
}

void loop() {
  // Read sensor data
  mpu.update();

  // Transmit data over Bluetooth
  bluetooth.print("X: "); bluetooth.print(mpu.getAccX());
  bluetooth.print(" Y: "); bluetooth.print(mpu.getAccY());
  bluetooth.print(" Z: "); bluetooth.println(mpu.getAccZ());

  // Short delay
  delay(100);
}"""

st.code(code, language="c++")

st.title("ultrasonic in raspberrypi")
code ="""const int trigPin = 18; // GPIO18
const int echoPin = 24; // GPIO24

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // Send a 10µs pulse to the TRIG pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure the duration of the ECHO signal
  long duration = pulseIn(echoPin, HIGH);

  // Calculate distance in centimeters
  float distance = (duration / 2.0) * 0.0343;

  // Print distance to Serial Monitor
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(1000); // 1-second delay
}"""

st.code(code, language="c++")

st.title("Arduino")
code ="""

1. Arduino with Potentiometer

int potPin = A0; // Connect the middle pin of the potentiometer to A0

void setup() {
  Serial.begin(9600); // Start the Serial Monitor
}

void loop() {
  int potValue = analogRead(potPin); // Read the analog value (0-1023)
  Serial.print("Potentiometer Value: ");
  Serial.println(potValue);
  delay(100); // Small delay to stabilize reading
}
```

---

2. Arduino with Servo Motor

#include <Servo.h>

Servo myServo; // Create a Servo object
int potPin = A0; // Potentiometer pin

void setup() {
  myServo.attach(9); // Attach servo to pin 9
}

void loop() {
  int potValue = analogRead(potPin); // Read potentiometer value
  int angle = map(potValue, 0, 1023, 0, 180); // Map to servo range
  myServo.write(angle); // Move servo to angle
  delay(15); // Allow the servo to reach the position
}
```

---

3. Arduino with IR Sensor

int irPin = 2; // IR sensor output pin
int ledPin = 13; // LED for indicator

void setup() {
  pinMode(irPin, INPUT);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  int irValue = digitalRead(irPin); // Read IR sensor value (HIGH or LOW)
  if (irValue == LOW) { // Obstacle detected
    digitalWrite(ledPin, HIGH); // Turn on LED
  } else {
    digitalWrite(ledPin, LOW); // Turn off LED
  }
}
```

---
4. Arduino with Stepper Motor

#include <Stepper.h>

const int stepsPerRevolution = 200; // Steps per revolution for your stepper motor

Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11); // Connect to pins 8, 10, 9, 11

void setup() {
  myStepper.setSpeed(60); // Set motor speed (RPM)
}

void loop() {
  myStepper.step(stepsPerRevolution); // Move one revolution forward
  delay(1000); // Wait 1 second
  myStepper.step(-stepsPerRevolution); // Move one revolution backward
  delay(1000); // Wait 1 second
}
```

---

5. Arduino with Any Analog Sensor (e.g., Temperature Sensor LM35)

const int tempPin = A0; // Analog pin connected to the sensor

void setup() {
  Serial.begin(9600); // Start the Serial Monitor
}

void loop() {
  int sensorValue = analogRead(tempPin); // Read analog value (0-1023)
  float voltage = sensorValue * (5.0 / 1023.0); // Convert to voltage
  float temperature = voltage * 100.0; // Convert to temperature (Celsius)
  
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");
  delay(1000); // 1-second delay
}
"""
st.code(code, language="c++")
