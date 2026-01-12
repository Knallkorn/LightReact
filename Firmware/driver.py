import serial
from time import sleep
import numpy
from matplotlib.colors import hsv_to_rgb

numLeds = 140
numRGB = numLeds * 3

startMarker = 0x0F
endMarker = 0xF0

hue = 0

link = serial.Serial(port='COM6', baudrate=115200, timeout=1)
sleep(2)

colors = numpy.full(shape=(numLeds, 3), fill_value=[0.0, 1.0, 1.0])

denormalise = numpy.vectorize((lambda x: int(x*255)))

while True:
    
    hue += 1
    if hue == 256:
        hue = 0
    colors[:, 0] = numpy.full(shape=(numLeds), fill_value=hue/255)

    data = denormalise(hsv_to_rgb(colors).flatten()).astype(numpy.uint8)
    data = numpy.insert(data, 0, startMarker)
    data = numpy.append(data, endMarker)
    data = data.astype(dtype=numpy.uint8)

    packet = data.tobytes()
    link.write(packet)
    sleep(0.05)
    recData = link.read_all()
    #print(f"Sent: {packet}\n")
    #print(f"Recieved: {recData}")
    #print(f"Size: {len(leds.tolist())}")
    #print(f"Matching: {recData == leds.tobytes()}")
    print("Loop")