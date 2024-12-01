import streamlit as st

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