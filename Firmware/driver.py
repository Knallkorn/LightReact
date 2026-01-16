# Imports
import serial
from time import sleep
import numpy
from PIL import ImageGrab, Image

# Functions
def sampleScreen(width):
    img = ImageGrab.grab()
    img = img.resize((width,round(img.size[1]/5)), resample=Image.Resampling.BOX)
    size = img.size
    imgArr = numpy.array(img.get_flattened_data(), dtype=numpy.uint8).reshape((size[1],size[0],3))
    return numpy.floor(imgArr.mean(axis=0)).astype(numpy.uint8)

def lerpColor(color1, color2, a):
    if not (0 <= a <= 1):
        a = max(0, min(1, a))
    lerped = [int(c1*(1 - a) + c2*a) for c1, c2 in zip(color1, color2)]
    return tuple(lerped)

# Initialise global variables
numLeds = 140

startMarker = 0x1

doLerp = True

colors = sampleScreen(numLeds)

# Initialise link
link = serial.Serial(port='COM6', baudrate=115200, timeout=1)
sleep(2)

# Main loop
while True:
    
    targetCol = sampleScreen(numLeds)
    if doLerp == True:
        for i in range(0, numLeds):
            colors[i] = lerpColor(colors[i], targetCol[i], 0.2)
    else:
        colors = sampleScreen(numLeds)
    colors[colors == 1] = 0

    # Package data
    data = colors
    data = numpy.insert(data, 0, startMarker)
    data = numpy.insert(data, 1, numLeds) # Number of LEDs (sending number of RGB values would be too large)

    # Send data
    packet = data.tobytes()
    link.write(packet)