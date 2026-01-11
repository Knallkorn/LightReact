#include <FastLED.h>
#include "SerialTransfer.h"

#define NUM_LEDS 140
#define LED_PIN 4
#define SIGNAL_PIN 8
#define DELAY 2

SerialTransfer txfer;

const size_t dataLength = NUM_LEDS*3;
uint8_t data[dataLength];
uint8_t packet = 0;

int time;

CRGB leds [NUM_LEDS];
void setup() {
  Serial.begin(115200);
  txfer.begin(Serial);
  
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
  if (txfer.available()) {
    for (int32_t i=0; i < txfer.bytesRead; i++)
      txfer.packet.txBuff[i] = txfer.packet.rxBuff[i];

    txfer.sendData(txfer.bytesRead);

    uint8_t packLen = txfer.packet.txBuff[3]; // Get number of payload bytes

    if (txfer.packet.txBuff[1] == 0 && packet != 0) { // Check packet ID (held in second byte)
      packet = 0;
    } else packet++;
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

