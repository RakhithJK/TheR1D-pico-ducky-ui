# Pico Ducky UI
USB Rubber Ducky is a USB device that can be used to automate keystrokes. However, it is not very user-friendly. This fork aims to make it more user-friendly by providing a user interface, and simple installation script.

https://user-images.githubusercontent.com/16740832/235188924-b9c13f64-9b40-400f-bd50-f5fb4c09eef2.mp4

## Requirements
To create you own USB Rubber Ducky, you will need the following:
* Waveshare ESP32-S2 LCD.
* Installed CircuitPython 8.x ([instructions](https://circuitpython.org/board/waveshare_esp32_s2_pico_lcd/)).
* Mac/Linux or Windows with WSL.

## Installation
Once you have Waveshare ESP32-S2 LCD with CircuitPython installed, follow these steps:
1. Clone this repository `git clone https://github.com/TheR1D/pico-ducky-ui`
1. Cd into the directory `cd pico-ducky-ui`
1. Connect the device to your computer.
1. Run `./install.sh` it might prompt you for path to CIRCUITPY.
1. Wait for the script to finish.
1. Reboot the device.

## Adding scripts
You can add your scripts by copying them to the `scripts` directory. It is recommended to use short names for the scripts, as the UI will only show the first several characters.

## Usage
Use "boot" button to switch between scripts (down direction). Select the script you would like to execute then hold "boot" button for 1 second and release.
