import serial
import time
import numpy

numLeds = 140
numRGB = numLeds * 3
dataLen = numRGB if numRGB % 64 == 0 else numRGB + (64-(numRGB%64))

link = serial.Serial(port='COM6', baudrate=115200, timeout=1)
time.sleep(2)

leds = numpy.full(shape=(numLeds), fill_value=255, dtype=numpy.uint8)
leds = leds.flatten()
split = list()
for i in range(numLeds // 64):
    split.append(64+(64*(i)))
leds = numpy.split(leds, split)

for packArr in leds:
    packData = packArr.tobytes()
    print(f"Sent: {packData}")
    link.write(packData)
    time.sleep(0.1)
    recData = link.read_all()
    print(f"Recieved: {recData}")
    print(f"Matching: {recData == packData}")