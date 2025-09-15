import usb_hid
from adafruit_hid.mouse import Mouse
from time import sleep
import board
import digitalio

import usb_hid
import usb_cdc
from time import sleep
import board
import digitalio

# State variables
left_button_down = False
right_button_down = False
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Initialize mouse and serial
mouse = Mouse(usb_hid.devices)
serial = usb_cdc.data

while True:
    if serial.in_waiting > 0:
        try:
            print("Listening on uart...")
            raw_data = serial.read(serial.in_waiting)
            if not raw_data:
                continue

            led.value = True
            msg = raw_data.decode("utf-8").strip()
            print("Received:", msg)

            # Expected format: dx,dy,scroll,left_click,right_click
            dx, dy, scroll, left_click, right_click = [int(i) for i in msg.split(",")]
#500,100,0,1,0 =
            # Mouse movement
            mouse.move(dx, dy, scroll)

            # Right click
            if right_click == 0 and right_button_down:
                mouse.release(Mouse.RIGHT_BUTTON)
                right_button_down = False
            elif right_click == 1:
                if right_button_down:
                    mouse.release(Mouse.RIGHT_BUTTON)
                    sleep(0.1)
                mouse.press(Mouse.RIGHT_BUTTON)
                right_button_down = True

            # Left click behaves same as right click
            if left_click == 0 and left_button_down:
                mouse.release(Mouse.LEFT_BUTTON)
                left_button_down = False
            elif left_click == 1:
                if left_button_down:
                    mouse.release(Mouse.LEFT_BUTTON)
                    sleep(0.1)
                mouse.press(Mouse.LEFT_BUTTON)
                left_button_down = True

        except Exception as e:
            print("Error:", e)
            led.value = False
    else:
        led.value = False
        sleep(0.05)
