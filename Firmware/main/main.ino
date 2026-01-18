// Includes and macros
#include <FastLED.h>

#define NUM_LEDS 140
#define NUM_RGB NUM_LEDS*3
#define LED_PIN 4
#define SIGNAL_PIN 8

#define START_MARKER 0x1 // 00000001

// Initalise global variables
const size_t dataLength = NUM_RGB;
uint8_t data[dataLength];
bool newData = false;

CRGB leds [NUM_LEDS];
uint8_t brightness = 50;

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
  FastLED.clear(true);
  FastLED.setBrightness(50); // Currently only static brightness at 50
}

void loop() {
  rcxData();
  echoData(); 
}

void rcxData() {
  static bool rcxCur = false; // Whether currently recieving
  static uint8_t metaData = 0; // Whether next byte should be payload
  static uint16_t ndx = 0; // Data index iterator
  static uint16_t payloadLength = 0; // Length of payload
  uint8_t rcx; // Buffer to hold serial input
  

  while (Serial.available() > 0 && newData == false) {
    rcx = Serial.read(); // Assuming that processing speed is considerably higher than baud, so only one byte to process at a time
    
    if (rcxCur == true) {
      if (ndx < payloadLength) { // Payload handling
        data[ndx] = rcx;
        ndx++;
      } else { // End of packet
        rcxCur = false;
        ndx = 0;
        payloadLength = 0;
        newData = true;
      }
    } else if (metaData == 1) {
      if (rcx == 0) {
        FastLED.clear(true);
        delay(100);
        digitalWrite(SIGNAL_PIN, LOW);
      } else {
        digitalWrite(SIGNAL_PIN, HIGH);
        payloadLength = ((uint16_t)rcx)*3;
      }
      metaData = 2;
    } else if (metaData == 2) {
        brightness = rcx;
        rcxCur = true;
        metaData = 0;
    } else if (rcx == START_MARKER) { // Begin packet
      metaData = 1;
    }
  }
}

void echoData() {
  if (newData == true) { // Only update LEDs if there a new packet has been processed
    for (int i=0; i<NUM_LEDS; i++) {
      leds[i].setRGB(data[(i*3)],data[(i*3)+1],data[(i*3)+2]);
    }
    FastLED.setBrightness(brightness);
    FastLED.show();
    newData = false;
  }
}
