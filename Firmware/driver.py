# Imports
import serial
from time import sleep
import numpy
from PIL import ImageGrab, Image

# Functions
def sampleScreen(width):
    img = ImageGrab.grab()
    img = img.resize((width,round(img.size[1]/3)), resample=Image.Resampling.BOX)
    size = img.size
    imgArr = numpy.array(img.get_flattened_data(), dtype=numpy.uint8).reshape((size[1],size[0],3))
    return numpy.floor(imgArr.mean(axis=0)).astype(numpy.uint8)

# Initialise global variables
numLeds = 140

startMarker = 0x1

colors = numpy.full(shape=(numLeds, 3), fill_value=0, dtype=numpy.uint8)

# Initialise link
link = serial.Serial(port='COM6', baudrate=115200, timeout=1)
sleep(2)

# Main loop
while True:
    
    colors = sampleScreen(numLeds)
    colors[colors == 1] = 0

    # Package data
    data = colors
    data = numpy.insert(data, 0, startMarker)
    data = numpy.insert(data, 1, numLeds) # Number of LEDs (sending number of RGB values would be too large)

    # Send data
    packet = data.tobytes()
    link.write(packet)
    # Sleep commented out for now as sampling screen should provide enough time. If moved to another thread, reimplement
    sleep(0.01)