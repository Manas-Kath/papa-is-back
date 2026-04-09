import time
import usb_hid
import board
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Initialize RGB LED on GP25
pixel = neopixel.NeoPixel(board.GP25, 1, brightness=0.1)
pixel.fill((255, 0, 0)) # RED = Hardware Initialized

# CRITICAL: Wait 5 seconds for Windows to finish recognizing COM12 and HID
time.sleep(5)

# Check for HID stack
if not usb_hid.devices:
    pixel.fill((255, 255, 0)) # YELLOW = HID Driver Error
    while True: pass

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
pixel.fill((0, 255, 0)) # GREEN = Ready to Strike

# Strike Sequence
kbd.send(Keycode.GUI, Keycode.R)
time.sleep(0.5)
layout.write("notepad")
time.sleep(0.2)
kbd.send(Keycode.ENTER)
time.sleep(1.5) # Give Notepad time to open

# Success Message
layout.write("RP2350-Zero HID Connection: SUCCESS\n")
layout.write("Engineering Mode: Active")
pixel.fill((0, 0, 255)) # BLUE = Mission Complete