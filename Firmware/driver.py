# Imports
import serial
from time import sleep
import numpy
from matplotlib.colors import hsv_to_rgb

# Initialise global variables
numLeds = 140

startMarker = 0x0F
endMarker = 0xF0

hue = 0

colors = numpy.full(shape=(numLeds, 3), fill_value=[0.0, 1.0, 1.0])

denormalise = numpy.vectorize((lambda x: int(x*255)))

# Initialise link
link = serial.Serial(port='COM6', baudrate=115200, timeout=1)
sleep(2)

# Main loop
while True:
    
    # TEMP - Rainbow loop
    hue += 1
    if hue >= 256:
        hue = 0
    colors[:, 0] = numpy.full(shape=(numLeds), fill_value=hue/255)

    # Package data
    data = denormalise(hsv_to_rgb(colors).flatten()).astype(numpy.uint8)
    data = numpy.insert(data, 0, startMarker)
    data = numpy.append(data, endMarker)
    data = data.astype(dtype=numpy.uint8)

    # Send data
    packet = data.tobytes()
    link.write(packet)
    sleep(0.01)