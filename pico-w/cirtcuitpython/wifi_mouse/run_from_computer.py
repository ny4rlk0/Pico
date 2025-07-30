import socket
from time import sleep
# Nyarlko 2025 (c)
key = "picoMouse"
TCP_IP = "192.168.1.104"  # PICO Server IP Change This To Your PICO IP
TCP_PORT = 443            # PICO Server port
# Encrypt the data using key
def xor_crypt(data: bytes, key: str) -> bytes:
    key_bytes = key.encode("utf-8")
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])
def send(msg:str):
    # Call xor_crypt method to Encrypt data
    encrypted_message = xor_crypt(msg.encode(), key)
    print("ENCRYPTED MSG: ",encrypted_message)
    print("ENCRYPTION KEY: ",key)
    # Connect to pi using TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
    	sock.connect((TCP_IP,TCP_PORT))
    	sock.sendall(encrypted_message)
    	# Sleep half a second
    	sleep(0.1)
    except Exception as e: print(e)
    finally:
    	# Close TCP connection
    	sock.close()
# Mouse Movement
# Order: NEW:dx,   dy, scroll, right_click, soft_reset, left_click_duration
# Order: OLD:dx,dy,scroll,left,_click_duration,right_click, unlock_mass_storage
data =   "500,0,0,0,0,0"
send(data)
print("DECRYPTED MSG:",data)