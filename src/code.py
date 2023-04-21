import os
import board
import terminalio

from time import sleep, monotonic
from displayio import Group
from digitalio import DigitalInOut, Direction, Pull

from adafruit_display_text.label import Label
from adafruit_debouncer import Debouncer

from ui import ChoiceMenu
from duckyinpython import runScript


YELLOW = 0xFFFF00
VERTICAL_INTERVAL = 26

# Initiate boot button.
button = DigitalInOut(board.BUTTON)
button.direction = Direction.INPUT
button.pull = Pull.UP
d_button = Debouncer(button)

# Time in seconds to consider a long press.
long_press_time = 1.0
last_press_time = 0

# Initiate device display.
display = board.DISPLAY
group = Group()
display.show(group)
execute_group = Group()

# Define execution screen.
execute_group.append(
    Label(
        font=terminalio.FONT,
        scale=2,
        text="Executing...",
        x=12,
        y=38,
        color=YELLOW
    )
)

# Define menu choices.
choices = os.listdir("scripts")
choice_menu = ChoiceMenu(4, 12, choices, group)
selected = choice_menu.selected


# Main loop.
while True:
    d_button.update()
    # Button pressed
    if d_button.fell:
        last_press_time = monotonic()
    # Button released
    if d_button.rose:
        press_duration = monotonic() - last_press_time
        if press_duration >= long_press_time:
            # Long press.
            display.show(execute_group)
            runScript(f"scripts/{choices[choice_menu.selected]}")
            display.show(group)
        else:
            # Short press.
            if choice_menu.selected == len(choices) - 1:
                group.y += VERTICAL_INTERVAL * (len(choices) - 1) - (VERTICAL_INTERVAL * 2)
            elif choice_menu.selected > 1:
                group.y -= VERTICAL_INTERVAL
            choice_menu.select_next()

    sleep(0.01)
