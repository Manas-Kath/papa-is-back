import supervisor
import os
import time
import digitalio
import asyncio
import board
import neopixel
from duckyinpython import *

# Initialize the onboard RGB LED on GP25
# Waveshare RP2350-Zero uses a WS2812 RGB LED
pixel = neopixel.NeoPixel(board.GP25, 1)
pixel.brightness = 0.3
# Define status colors
COLOR_OFF = (0, 0, 0)
COLOR_IDLE = (0, 0, 50)    # Blue: Waiting/Ready
COLOR_RUNNING = (0, 50, 0) # Green: Executing Payload
COLOR_SETUP = (50, 0, 0)   # Red: Setup Mode (GP0 grounded)
COLOR_EXFIL = (50, 25, 0)  # Orange: Exfiltrating Data

# WiFi support check
IS_WIFI_BOARD = board.board_id in ['raspberry_pi_pico_w', 'raspberry_pi_pico2_w']

def startWiFi():
    """Initializes WiFi AP if the hardware supports it."""
    if not IS_WIFI_BOARD:
        return
    import wifi
    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets missing in secrets.py")
        return

    print("Starting Access Point")
    wifi.radio.start_ap(secrets['ssid'], secrets['password'])
    print("AP IP:", wifi.radio.ipv4_address_ap)

# Disable autoreload to prevent interruptions during file operations
supervisor.runtime.autoreload = False

async def run_payload_on_startup():
    """Checks for programming mode and runs the payload if appropriate."""
    progStatus = getProgrammingStatus()
    print("Board ID:", board.board_id)
    print("Programming Status:", progStatus)
    
    if not progStatus:
        print("Finding payload...")
        for _ in range(5):
            pixel.fill((0, 0, 255))
            await asyncio.sleep(0.2)
            pixel.fill((0, 0, 0))
            await asyncio.sleep(0.2)
        # Skip execution if exfiltrated data already exists to prevent loops
        if "loot.bin" in os.listdir("/"):
            print("loot.bin detected, skipping execution.")
            pixel.fill(COLOR_IDLE)
        else:
            payload = selectPayload()
            await asyncio.sleep(5) # Short delay for host recognition
            print("Running:", payload)
            
            pixel.fill(COLOR_RUNNING) # Visual Clue: Green while running
            await runScript(payload)
            pixel.fill(COLOR_IDLE)    # Visual Clue: Blue when done
            print("Payload Finished")
    else:
        print("Setup Mode Active - No payload will run.")
        pixel.fill(COLOR_SETUP)

async def status_indicator_task():
    """Periodic task to update LED based on global state."""
    while True:
        progStatus = getProgrammingStatus()
        exfil_active = variables.get("$_EXFIL_MODE_ENABLED", False)
        
        if progStatus:
            pixel.fill(COLOR_SETUP)
        elif exfil_active:
            pixel.fill(COLOR_EXFIL)
        
        await asyncio.sleep(0.2)

async def main_loop():
    """Gathers all asynchronous tasks for the ducky operation."""
    global button1
    
    tasks = [
        asyncio.create_task(monitor_buttons(button1)),
        asyncio.create_task(run_payload_on_startup()),
        asyncio.create_task(monitor_led_changes()),
        asyncio.create_task(status_indicator_task())
    ]
    
    # Enable web services only on WiFi-capable boards
    if IS_WIFI_BOARD:
        from webapp import startWebService
        startWiFi()
        tasks.append(asyncio.create_task(startWebService()))
        
    await asyncio.gather(*tasks)

# Execution Start
print("Initializing Rubber Ducky...")
asyncio.run(main_loop())
