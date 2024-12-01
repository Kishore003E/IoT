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
