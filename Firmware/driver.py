import serial
import time
import numpy

numLeds = 140
numRGB = numLeds * 3

startMarker = 0x0F
endMarker = 0xF0

link = serial.Serial(port='COM6', baudrate=115200, timeout=1)
time.sleep(2)

leds = numpy.full(shape=(numLeds, 3), fill_value=255, dtype=numpy.uint8)
leds = leds.flatten()

data = leds
data = numpy.insert(data, 0, startMarker)
data = numpy.append(data, endMarker)
data = data.astype(dtype=numpy.uint8)

packet = data.tobytes()
print(f"Sent: {packet}\n")
link.write(packet)
time.sleep(0.05)
recData = link.read_all()
print(f"Recieved: {recData}")
print(f"Size: {len(leds.tolist())}")
print(f"Matching: {recData == leds.tobytes()}")