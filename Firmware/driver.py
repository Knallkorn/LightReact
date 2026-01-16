# IMPORTS
import serial
from time import sleep, time
import numpy
from matplotlib.colors import hsv_to_rgb
from math import sqrt
from PIL import ImageGrab, Image
from enum import Enum

# FUNCTIONS AND ENUMS
class LEDMode(Enum):
    REACTIVE = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    RAINBOW = 5

# Vectorised function that iterates over numpy array and multiplies each element by 255
# Intended to denormalise RGB values from range 0.0-0.1 to 0-255
denormalise = numpy.vectorize((lambda x: int(x*255)))

# Returns a numpy uint8 array of shape (width, 3) that contains the vertical average colour of the screen at each point
def sampleScreen(width: int):
    img = ImageGrab.grab()
    img = img.resize((width,round(img.size[1]/5)), resample=Image.Resampling.BOX)
    size = img.size
    imgArr = numpy.array(img.get_flattened_data(), dtype=numpy.uint8).reshape((size[1],size[0],3))
    return numpy.floor(imgArr.mean(axis=0)).astype(numpy.uint8)

# Lerps between 2 RGB tuples of format (R, G, B) at rate a and returns the interpolated colour
def lerpColor(color1: tuple, color2: tuple, a: float):
    if not (0 <= a <= 1):
        a = max(0, min(1, a))
    lerped = [int(c1*(1 - a) + c2*a) for c1, c2 in zip(color1, color2)]
    return tuple(lerped)

# Gets the average percieved brightness of a numpy array of RGB values of shape (..., 3)
def getBrightness(colors):
    avg = colors.mean(axis=0)
    # Percieved brightness magic numbers from https://alienryderflex.com/hsp.html
    return sqrt(0.299*(avg[0]**2) + 0.587*(avg[1]**2) + 0.114*(avg[2]**2))

# Screen-based reactive lighting logic
def getScreenCol(width: int, doLerp: bool=True, cols=None):
    if doLerp == True:
        targetCol = sampleScreen(width)
        for i, c in enumerate(cols):
            cols[i] = lerpColor(c, targetCol[i], lerpAlpha)
    else:
        cols = sampleScreen(width)
    return cols

# INITIALISE GLOBAL VARIABLES
mode = LEDMode.RAINBOW

numLeds = 140

startMarker = 0x1

doLerp = True
lerpAlpha = 0.2

reactiveBrightness = False
brightnessStatic = 50
brightnessMod = 1

colors = sampleScreen(numLeds)

delay = False

# INITALISE LINK
link = serial.Serial(port='COM6', baudrate=115200, timeout=1)
sleep(2)

# MAIN LOOP
while True:
    
    # Update RGB based on mode
    match mode:
        case LEDMode.REACTIVE:
            colors = getScreenCol(numLeds, doLerp, colors)
        case LEDMode.RED:
            colors = numpy.full(shape=(numLeds, 3), fill_value=[255, 0, 0], dtype=numpy.uint8)
        case LEDMode.GREEN:
            colors = numpy.full(shape=(numLeds, 3), fill_value=[0, 255, 0], dtype=numpy.uint8)
        case LEDMode.BLUE:
            colors = numpy.full(shape=(numLeds, 3), fill_value=[0, 0, 255], dtype=numpy.uint8)
        case LEDMode.RAINBOW:
            hue = (round(time()*15) % 256)/255
            colors = numpy.full(shape=(numLeds, 3), fill_value=[0.0, 1.0, 1.0])
            colors[:, 0] = numpy.full(shape=(numLeds), fill_value=hue)
            colors = denormalise(hsv_to_rgb(colors)).astype(numpy.uint8)
        case _:
            colors = numpy.full(shape=(numLeds, 3), fill_value=[0, 255, 0], dtype=numpy.uint8)

    # Update brightness
    if reactiveBrightness == True:
        brightness = getBrightness(colors)*brightnessMod
    else:
        brightness = brightnessStatic

    # Package data
    data = colors
    data[data == 1] = 0 # Ensure no bytes match marker (Causes issues)
    data = numpy.insert(data, 0, startMarker)
    data = numpy.insert(data, 1, numLeds) # Number of LEDs (sending number of RGB values would be too large)
    data = numpy.insert(data, 2, brightness)

    # Send data
    packet = data.tobytes()
    link.write(packet)
    if delay == True:
        sleep(0.02)