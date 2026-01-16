# Imports
import serial
from time import sleep
import numpy
from math import sqrt
from PIL import ImageGrab, Image

# Functions
def sampleScreen(width: int):
    img = ImageGrab.grab()
    img = img.resize((width,round(img.size[1]/5)), resample=Image.Resampling.BOX)
    size = img.size
    imgArr = numpy.array(img.get_flattened_data(), dtype=numpy.uint8).reshape((size[1],size[0],3))
    return numpy.floor(imgArr.mean(axis=0)).astype(numpy.uint8)

def lerpColor(color1: tuple, color2: tuple, a: float):
    if not (0 <= a <= 1):
        a = max(0, min(1, a))
    lerped = [int(c1*(1 - a) + c2*a) for c1, c2 in zip(color1, color2)]
    return tuple(lerped)

def getBrightness(colors):
    avg = colors.mean(axis=0)
    # Percieved brightness magic numbers from https://alienryderflex.com/hsp.html
    return sqrt(0.299*(avg[0]**2) + 0.587*(avg[1]**2) + 0.114*(avg[2]**2))

# Initialise global variables
numLeds = 140

startMarker = 0x1

doLerp = True
lerpAlpha = 0.2

brightnessMod = 1

colors = sampleScreen(numLeds)

# Initialise link
link = serial.Serial(port='COM6', baudrate=115200, timeout=1)
sleep(2)

# Main loop
while True:
    
    if doLerp == True:
        targetCol = sampleScreen(numLeds)
        for i, c in enumerate(colors):
            colors[i] = lerpColor(c, targetCol[i], lerpAlpha)
    else:
        colors = sampleScreen(numLeds)
    
    colors[colors == 1] = 0 # Ensure no bytes match start marker

    brightness = getBrightness(colors)*brightnessMod
    

    # Package data
    data = colors
    data = numpy.insert(data, 0, startMarker)
    data = numpy.insert(data, 1, numLeds) # Number of LEDs (sending number of RGB values would be too large)
    data = numpy.insert(data, 2, brightness)

    # Send data
    packet = data.tobytes()
    link.write(packet)