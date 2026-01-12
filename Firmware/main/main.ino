// Includes and macros
#include <FastLED.h>

#define NUM_LEDS 140
#define NUM_RGB NUM_LEDS*3
#define LED_PIN 4
#define SIGNAL_PIN 8

#define START_MARKER 0x0F // 00001111
#define END_MARKER 0xF0 // 11110000

// Initalise global variables
const size_t dataLength = NUM_RGB;
uint8_t data[dataLength];
bool newData = false;

CRGB leds [NUM_LEDS];

void setup() {
  // Initialise serial
  Serial.begin(115200);
  Serial.setTimeout(1);

  // Relay control
  pinMode(SIGNAL_PIN, OUTPUT);
  digitalWrite(SIGNAL_PIN, HIGH);
  delay(100); // Delay to ensure LEDs are booted before data sent
  
  // Initialise LEDs
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds,NUM_LEDS);
  FastLED.clear();
  FastLED.setBrightness(50); // Currently only static brightness at 50
}

void loop() {
  rcxData();
  echoData(); 
}

void rcxData() {
  static bool rcxCur = false; // Whether currently recieving
  static uint16_t ndx = 0; // Data index iterator
  uint8_t rcx; // Buffer to hold serial input

  while (Serial.available() > 0 && newData == false) {
    rcx = Serial.read(); // Assuming that processing speed is considerably higher than baud, so only one byte to process at a time

    if (rcxCur == true) {
      if (rcx != END_MARKER) { // Payload handling
        data[ndx] = rcx;
        ndx++;
        if (ndx >= dataLength) {
          ndx = dataLength - 1;
        }
      } else { // End of packet
        rcxCur = false;
        ndx = 0;
        newData = true;
      }
    } else if (rcx == START_MARKER) { // Begin packet
      rcxCur = true;
    }
  }
}

void echoData() {
  if (newData == true) { // Only update LEDs if there a new packet has been processed
    for (int i=0; i<NUM_LEDS; i++) {
      leds[i].setRGB(data[(i*3)],data[(i*3)+1],data[(i*3)+2]);
    }
    FastLED.show();
    newData = false;
  }
}
