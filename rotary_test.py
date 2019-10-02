from time import sleep_ms
from encoder import Encoder
from machine import Pin

#pin1 = Pin(21, Pin.IN)

def main():
    enc = Encoder(23, 19)
    lastval = 0

    while True:
        #print(pin1.value())
        val = enc.value
        if lastval != val:
            lastval = val
            print(val)
        sleep_ms(50)


main()