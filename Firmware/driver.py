from pySerialTransfer import pySerialTransfer as txfer
import time
import numpy

numLeds = 140
numRGB = numLeds * 3
leds = numpy.arange(numRGB, dtype=numpy.uint16) #numpy.full(shape=numRGB, fill_value=255, dtype=numpy.uint8)
leds = numpy.array_split(leds, (numRGB // 64)+1)

try:
    link = txfer.SerialTransfer('COM6', baud=115200)

    link.open()
    time.sleep(2)

    for i in range(len(leds)):
        ledList = leds[i].tolist()
        listSize = link.tx_obj(ledList)
        link.send(listSize, packet_id=i)

        while not link.available():
            if link.status.value < 0:
                print('ERROR: {}'.format(link.status))
        
        dataBack = link.rx_obj(obj_type=type(ledList), obj_byte_size=listSize, list_format='i')
        print(f"Recieved back: {dataBack}")

except KeyboardInterrupt:
    try:
        link.close()
    except:
        pass
except Exception as e:
    print(e)
    try:
        link.close()
    except:
        pass