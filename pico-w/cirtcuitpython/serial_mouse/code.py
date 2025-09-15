import usb_hid
from adafruit_hid.mouse import Mouse
from time import sleep
import usb_cdc
# State variables
left_button_down = False
right_button_down = False

# Initialize mouse and serial
mouse = Mouse(usb_hid.devices)
serial = usb_cdc.data
while True:
    if serial.in_waiting > 0:
        try:
            raw_data = serial.read(serial.in_waiting)
            if not raw_data:
                continue
            msg = raw_data.decode("utf-8").strip()
            # Expected format: dx,dy,scroll,left_click,right_click
            dx, dy, scroll, left_click, right_click = [int(i) for i in msg.split(",")]
            # Paste Putty Console to Example Movement 500,100,0,1,0
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
            # Left click
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
    else:
        sleep(0.05)
