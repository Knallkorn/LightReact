#include <FastLED.h>

#define NUM_LEDS 140
#define NUM_RGB NUM_LEDS*3
#define LED_PIN 4
#define SIGNAL_PIN 8

#define START_MARKER 0x0F // 00001111
#define END_MARKER 0xF0 // 11110000

const size_t dataLength = NUM_RGB;
uint8_t data[dataLength];
bool newData = false;

CRGB leds [NUM_LEDS];

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  pinMode(SIGNAL_PIN, OUTPUT);
  digitalWrite(SIGNAL_PIN, HIGH);
  delay(100);
  
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds,NUM_LEDS);
  FastLED.clear();
  FastLED.setBrightness(50);
  for (int i=0; i<NUM_LEDS; i++) {
    leds[i].setHSV(0, 255, 0);
  }
  FastLED.show();
}

void loop() {
  rcxData();
  echoData(); 
}

void rcxData() {
  static bool rcxCur = false;
  static uint16_t ndx = 0;
  uint8_t rcx;

  while (Serial.available() > 0 && newData == false) {
    rcx = Serial.read();

    if (rcxCur == true) {
      if (rcx != END_MARKER) {
        data[ndx] = rcx;
        ndx++;
        if (ndx >= dataLength) {
          ndx = dataLength - 1;
        }
      } else {
        rcxCur = false;
        ndx = 0;
        newData = true;
      }
    } else if (rcx == START_MARKER) {
      rcxCur = true;
    }
  }
}

void echoData() {
  if (newData == true) {
    //Serial.write(data, dataLength);
    for (int i=0; i<NUM_LEDS; i++) {
      leds[i].setRGB(data[(i*3)],data[(i*3)+1],data[(i*3)+2]);
    }
    FastLED.show();
    newData = false;
  }
}
