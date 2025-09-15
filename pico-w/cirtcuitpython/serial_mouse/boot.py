# boot.py
import os

#Emulate Mouse
import usb_hid
import usb_cdc
usb_cdc.enable(data=True, console=False)
# Other Example Options
# usb_hid.Device.KEYBOARD
# usb_hid.Device.CONSUMER_CONTROL
# usb_hid.Device.MOUSE

# Enable HID, you need extra (,) comma here python to see this as tuple
# Default HID Descriptors
# Enable Custom Definitions Defined above
usb_hid.enable((usb_hid.Device.MOUSE,))
