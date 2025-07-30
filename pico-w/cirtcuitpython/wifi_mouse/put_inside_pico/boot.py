# boot.py
import usb_cdc
import storage
import os
import supervisor
import usb_midi
import board
import digitalio
import microcontroller

#Emulate Mouse
import usb_hid

# Example Mouse descriptor
mouse_descriptor = bytes([
    0x05, 0x01, 0x09, 0x02,       # Usage Page (Generic Desktop), Usage (Mouse)
    0xA1, 0x01,                   # Collection (Application)
    0x85, 0x01,                   # Report ID = 1
    # Simplified button + XY movement
    0x05, 0x09, 0x19, 0x01, 0x29, 0x03,
    0x15, 0x00, 0x25, 0x01, 0x75, 0x01, 0x95, 0x03, 0x81, 0x02,
    0x75, 0x05, 0x95, 0x01, 0x81, 0x03,
    0x05, 0x01, 0x09, 0x30, 0x09, 0x31,
    0x15, 0x81, 0x25, 0x7F, 0x75, 0x08, 0x95, 0x02, 0x81, 0x06,
    0xC0                                # End Collection
])

# Example Mouse Interface Report Descriptor
mouse_interface = usb_hid.Device(
    report_descriptor=mouse_descriptor,
    usage_page=0x01,
    usage=0x02,
    report_ids=(1,),
    in_report_lengths=(4,),
    out_report_lengths=(0,)
)

# Example Consumer Control Descriptor
consumer_descriptor = bytes([
    0x05, 0x0C,       # Usage Page (Consumer Devices)
    0x09, 0x01,       # Usage (Consumer Control)
    0xA1, 0x01,
    0x85, 0x02,       # Report ID = 2
    0x15, 0x00, 0x25, 0x01,
    0x75, 0x01, 0x95, 0x08,
    0x09, 0xE9,       # Usage (Volume Up)
    0x09, 0xEA,       # Usage (Volume Down)
    0x09, 0xE2,       # Usage (Mute)
    0x09, 0xCD,       # Usage (Play/Pause)
    0x09, 0xB5,       # Usage (Scan Next)
    0x09, 0xB6,       # Usage (Scan Previous)
    0x09, 0xB7,       # Usage (Stop)
    0x09, 0xB0,       # Usage (Rewind)
    0x81, 0x02,
    0xC0
])

# Example Consumer Interface Report Descriptor
consumer_interface = usb_hid.Device(
    report_descriptor=consumer_descriptor,
    usage_page=0x0C,
    usage=0x01,
    report_ids=(2,),
    in_report_lengths=(1,),
    out_report_lengths=(0,)
)

# Example Vendor HID Interface
vendor_descriptor1 = bytes([
  0x06,  0x00,  0xFF,  
  0x09,  0x02,  
  0xA1,  0x01,  
  0x85,  0x11,  
  0x15,  0x00,  
  0x25,  0x01,  
  0x35,  0x00,  
  0x45,  0x01,  
  0x65,  0x00,  
  0x55,  0x00,  
  0x75,  0x01,  
  0x95,  0x98,  
  0x81,  0x03,  
  0x91,  0x03,  
  0xC0                # End Collection
])

# Example Vendor HID Interface Report Descriptor
vendor1 = usb_hid.Device(
    report_descriptor=vendor_descriptor1,
    usage_page=0xFF,
    usage=0x02,
    report_ids=(0x11,),         # Must match 0x85
    in_report_lengths=(19,),
    out_report_lengths=(19,)
)


# ---------- Vendor HID Interface 2 ----------
vendor_descriptor2 = bytes([
  0x06,  0x00,  0xFF,  
  0x09,  0x01,  
  0xA1,  0x01,  
  0x85,  0x10,  
  0x15,  0x00,  
  0x25,  0x01,  
  0x35,  0x00,  
  0x45,  0x01,  
  0x65,  0x00,  
  0x55,  0x00,  
  0x75,  0x01,  
  0x95,  0x98,  
  0x81,  0x03,  
  0x91,  0x03,  
  0xC0                # End Collection
])

vendor2 = usb_hid.Device(
    report_descriptor=vendor_descriptor2,
    usage_page=0xFF,
    usage=0x01,
    report_ids=(0x10,),         # Must match 0x85
    in_report_lengths=(19,),
    out_report_lengths=(19,)
)

# Unlock USB Mass Storage if We receive (0,0,0,0,0,1) aka Unlock USB MS
# Check if we have something in memory saved between reboots
if microcontroller.nvm[0] != 1:
    # If we dont have, Disable CIRTCUITPYTHON USB DRIVE
    usb_cdc.disable()
    storage.disable_usb_drive()

# Disable MiDi
usb_midi.disable()

# Custom USB Identifier Example
#supervisor.set_usb_identification(
#    manufacturer="Logitech",
#    product="USB Receiver", # USB Receiver = Logitech, G300s Optical Gaming Mouse
#    vid=0x046D,     # Custom VID 0x046D = Logitech Brand, HEX Value
#    pid=0xC52F      # Custom PID  0xC52F = M330 Logitech, 0xC246 = G300s Optical Gaming Mouse
#)

# Example for Setting Interface Name
#usb_hid.set_interface_name("Logitech HID Interface")

# Other Example Options
#usb_hid.Device.KEYBOARD
#usb_hid.Device.CONSUMER_CONTROL

# Enable HID, you need extra (,) comma here python to see this as tuple
# Default HID Descriptors, not anything up there
usb_hid.enable((usb_hid.Device.MOUSE,))

# Enable Custom Definitions Defined above
#usb_hid.enable((mouse_interface,consumer_interface,vendor1,vendor2))

# Clear memory that save data between reboots
if microcontroller.nvm[0] == 1:
    microcontroller.nvm[0] = 0