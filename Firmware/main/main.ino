#include <FastLED.h>

#define NUM_LEDS 140
#define NUM_RGB NUM_LEDS*3
#define LED_PIN 4
#define SIGNAL_PIN 8
#define DELAY 2

const size_t dataLength = NUM_RGB;
uint8_t data[dataLength];

int time;

CRGB leds [NUM_LEDS];

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  
  /*
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds,NUM_LEDS);
  FastLED.clear();
  FastLED.setBrightness(50);
  time = 0;
  for (int i=0; i<NUM_LEDS; i++) {
    leds[i].setHSV(0, 255, 255);
  }
  FastLED.show();

  pinMode(SIGNAL_PIN, OUTPUT);
  digitalWrite(SIGNAL_PIN, HIGH);
  */
}

void loop() {
  if (Serial.available() > 0) {
    byte packData[64];
    int packLen = Serial.readBytes(packData, Serial.available());
    Serial.write(packData, packLen);
  }

  /*
  for (int i=0; i<NUM_LEDS; i++) {
    leds[i].setHue((i + time > 255 ? time+i-255 : time + i));
  }
  FastLED.show();
  if (time++ > 255) {
    time = 0;
  }

  Serial.println();
  delay(DELAY);
  */
}

