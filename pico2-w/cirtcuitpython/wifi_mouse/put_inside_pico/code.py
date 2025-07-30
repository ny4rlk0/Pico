import usb_hid
import wifi
import socketpool
import array
from adafruit_hid.mouse import Mouse
from time import sleep
import microcontroller
import board
import digitalio
import supervisor

# Customize Variables
key = "picoMouse"  # Must match client key!
SSID = "WIFI_SSID"
PW = "WIFI_PASSWORD"
PORT= 443
# Do not change variables
left_button_down = False
right_button_down = False
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
# Basic encryption method
def xor_crypt(data: bytes, key: str) -> bytes:
    key_bytes = key.encode("utf-8")
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])
print("Device started...")
# Connect to Wi-Fi
try:
    print("Connecting to Wi-Fi...")
    wifi.radio.connect(SSID, PW)
except Exception as e:
    #print("Error: ",e)
    print("Soft Rebooting...")
    for i in range (5):
        led.value = True
        sleep(0.2)
        led.value = False
        sleep(0.2)
    microcontroller.reset()

led.value = True

pool = socketpool.SocketPool(wifi.radio)
# Start TCP server
server = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
server.bind(("0.0.0.0", PORT))
server.listen(1)

mouse = Mouse(usb_hid.devices)

while True:
    print("Wi-Fi:",str(wifi.radio.ipv4_address)+":"+str(PORT),"\nWaiting for client...")
    conn, addr = server.accept()
    conn.settimeout(None)    # None means “wait forever”
    print("Received data from ", addr)
    while True:
        try:
            buf = array.array("b", [0] * 32)
            recv_size = conn.recv_into(buf)
            data = bytes(buf[:recv_size])  # convert to normal bytes
            if not data:
                print("Client disconnected")
                led.value=False
                break
            else: led.value=True
            print("Encrypted data: ",data)
            #Decrypt data first.
            decrypted_data = xor_crypt(data, key)
            msg = decrypted_data.decode("utf-8").strip()
            print("Decrypted data: ", msg)  # Debug
            dx, dy, scroll , left_click_duration, right_click, unlock_mass_Storage= [int(i) for i in msg.split(",")]
            # Maintenance mode open USB MASS STORAGE from server then replug it the pi
            # To disable MASS STORAGE delete usb_unlock file replug the pi
            try:
                if unlock_mass_Storage==1:
                    microcontroller.nvm[0] = 1  # Say “unlock CIRCUITPY for one boot”
                    microcontroller.reset()     # Reboot Pico W
            except Exception as e:
                print(e)
            mouse.move(dx, dy, scroll)
            if right_click == 0 and right_button_down:
                mouse.release(Mouse.RIGHT_BUTTON)
                right_button_down = False
            if right_click == 1:
                if right_button_down: 
                    right_button_down = False
                    mouse.release(Mouse.RIGHT_BUTTON)
                    sleep(0.1)
                mouse.press(Mouse.RIGHT_BUTTON)
                right_button_down = True
                #sleep(0.1)
                #right_button_down = False
                #mouse.release(Mouse.RIGHT_BUTTON)
                #sleep(0.2)
            if left_click_duration > 0:
                mouse.press(Mouse.LEFT_BUTTON)
                left_button_down = True
                sleep(left_click_duration/1000)
                mouse.release(Mouse.LEFT_BUTTON)
                left_button_down = False
        except Exception as e:
            print("Error:", e)
            break
    # Add this BEFORE conn.close to allow time
    sleep(0.1)
    conn.close()
