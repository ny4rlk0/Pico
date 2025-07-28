from board import LED
from digitalio import DigitalInOut, Direction
from time import sleep
led = DigitalInOut(LED)
led.direction = Direction.OUTPUT
while True:
    led.value = True
    sleep(0.2)
    led.value = False
    sleep(0.2)
