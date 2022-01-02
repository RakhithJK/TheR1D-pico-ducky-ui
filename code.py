import os
import board
import time
import terminalio
import displayio
import busio
import adafruit_st7789
from adafruit_display_text import label
from digitalio import DigitalInOut, Direction, Pull
import ducky


displayio.release_displays()
TFT_CS = board.GP17
TFT_DC = board.GP16
SPI_MOSI = board.GP19
SPI_CLK = board.GP18
SPI = busio.SPI(SPI_CLK, MOSI=SPI_MOSI)
DISPLAY_BUS = displayio.FourWire(SPI, command=TFT_DC, chip_select=TFT_CS)

display = adafruit_st7789.ST7789(DISPLAY_BUS, width=135, height=240, rowstart=40, colstart=53)
display.rotation = 270
splash = displayio.Group()
display.show(splash)

RED = 0xFF0000
WHITE = 0xFFFFFF
DUCKY_SCRIPT_FOLDER = "./ducky_scripts"
DUCKY_SCRIPT_NAMES = os.listdir(DUCKY_SCRIPT_FOLDER)

def draw_text(x, y, scale, text, color):
    return label.Label(terminalio.FONT, text=text, color=color, scale=scale, x=x, y=y)

VERTICAL_INTERVAL = 30 # Interval between menu choices (scripts).
running_interval = 10 # Running interval will be incrementing in loop.
selected = 0 # Currently selected script.
for index, script_name in enumerate(DUCKY_SCRIPT_NAMES):
    # Drawing menu choices (scripts).
    text = str(index + 1) + ". " + script_name.replace(".dd", "")
    color = RED if index == selected else WHITE
    label_text = draw_text(10, running_interval, 2, text, color)
    splash.append(label_text)
    running_interval += VERTICAL_INTERVAL
time.sleep(0.5)

# Create DigitalInOut and setup instance.
def make_button(pin_id):
    gp_pin = getattr(board, "GP" + str(pin_id))
    button = DigitalInOut(gp_pin)
    button.direction = Direction.INPUT
    button.pull = Pull.UP
    return button

# Create callback for given button.
def button_callback(button_name, button, callback):
    prev_state = globals().get(button_name + "_prev_state")
    if prev_state is not None and button.value != prev_state:
        button_name_upper = button_name.upper()
        if not button.value:
            callback(button_name)
            print("Button " + button_name_upper + " is pressed.")
        else:
            print("Button " + button_name_upper + " is unpressed.")
    globals()[button_name + "_prev_state"] = button.value

# Map of button names => GP ID.
buttons_map = {"a": 12, "b": 13, "x": 14, "y": 15}
# Create defined DigitalInOut instances using map.
for name, gp_id in buttons_map.items():
    globals()["button_" + name] = make_button(gp_id)

def main_callback(button_name):
    print("Callback for: " + button_name)
    global selected
    if button_name == "b":
        splash[selected].color = WHITE
        selected = selected + 1 if selected < len(DUCKY_SCRIPT_NAMES) - 1 else 0
        splash[selected].color = RED
        if selected > 2:
            splash.y -= VERTICAL_INTERVAL
        elif selected == 0:
            splash.y = 0
    elif button_name == "a":
        splash[selected].color = WHITE
        selected = selected - 1 if selected > 0 else len(DUCKY_SCRIPT_NAMES) - 1
        splash[selected].color = RED
        if selected == len(DUCKY_SCRIPT_NAMES) - 1:
            splash.y -= VERTICAL_INTERVAL * (len(DUCKY_SCRIPT_NAMES) - 1) - (VERTICAL_INTERVAL * 2)
        elif selected > 1:
            splash.y += VERTICAL_INTERVAL
    elif button_name == "x":
        ducky.execute(DUCKY_SCRIPT_FOLDER + "/" + DUCKY_SCRIPT_NAMES[selected], display)
        display.show(splash)

while True:
    for name in buttons_map.keys():
        button = globals()["button_" + name]
        button_callback(name, button, main_callback)
    time.sleep(0.05)
