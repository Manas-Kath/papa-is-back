# Pico Ducky - CircuitPython HID Injector

This project is a sophisticated USB Rubber Ducky (HID injector) implementation for CircuitPython, specifically optimized for Raspberry Pi Pico, Pico W, and RP2350-Zero boards. It features a full DuckyScript interpreter, a web-based management interface (on WiFi-enabled boards), and stealth capabilities.

## Project Overview

The project transforms a micro-controller into a powerful HID (Human Interface Device) that can execute automated keystroke payloads. Unlike simple injectors, it supports a rich subset of DuckyScript including logic and variables, and provides a web UI for remote payload management.

### Key Technologies
- **CircuitPython**: The core runtime environment.
- **DuckyScript**: The scripting language for HID payloads.
- **WSGI**: Used for the web management interface.
- **asyncio**: Manages concurrent tasks like the web server, button monitoring, and payload execution.

## Core Components

- **`duckyinpython.py`**: The heart of the project. It's a custom interpreter that parses and executes `.dd` (DuckyScript) files. It supports advanced features like `VAR`, `IF`, `WHILE`, `FUNCTION`, and random character generation.
- **`webapp.py` & `wsgiserver.py`**: Provides a mobile-friendly web interface (accessible via WiFi on Pico W) to:
    - List available payloads.
    - Create and edit DuckyScripts directly in the browser.
    - Trigger payloads remotely.
    - Delete scripts.
- **`boot.py`**: Handles low-level startup configuration. It can dynamically disable the USB mass storage device to prevent the host from seeing the "CIRCUITPY" drive, which is essential for stealth and data exfiltration.
- **`pins.py`**: Centralizes GPIO pin definitions for hardware buttons, payload selection switches, and programming mode detection.
- **`code.py`**: The main execution loop that initializes hardware, starts the web server, and handles payload triggers.

## Hardware Configuration

The project is designed to work with various GPIO-based triggers:
- **GP20**: Main execution button.
- **GP0**: Programming mode (grounding this pin disables automatic payload execution).
- **GP4, GP5, GP10, GP11**: Payload selection pins (allows choosing between 4 different `.dd` files).
- **GP15**: Stealth mode toggle (determines if the USB drive is visible to the host).
- **GP25**: RGB LED for status feedback (Red: Setup, Blue: Ready, Green: Running, Orange: Exfil).

## Development and Usage

### Adding Payloads
1. Connect the device in "Programming Mode" (ensure the USB drive is visible).
2. Copy your DuckyScript files (ending in `.dd`) to the root directory.
3. The default payload is `payload.dd`.

### Running the Web Interface (Pico W)
1. Ensure `secrets.py` (if required) or the `startWiFi` function in `code.py` is configured with your desired SSID and password.
2. Connect to the WiFi AP created by the Pico.
3. Navigate to the IP address (usually `192.168.4.1`) in your browser to manage scripts.

### Build and Test
As a CircuitPython project, there is no "build" step. Changes to `.py` files are automatically reloaded by the supervisor unless disabled.
- **Testing**: Use the `WAIT_FOR_BUTTON_PRESS` command in DuckyScript or the physical button on GP20 to trigger execution safely during testing.

## Directory Structure Notes
- **`lib/`**: Contains pre-compiled `.mpy` and source `.py` libraries for HID, WSGI, and debouncing.
- **`latest ducky/`**: Contains the most recent stable version of the full implementation.
- **Root Directory**: Contains the active files running on the device.
