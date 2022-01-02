import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_display_text import label
import displayio
import time
import digitalio
import terminalio
from board import *

duckyCommands = ["WINDOWS", "GUI", "APP", "MENU", "SHIFT", "ALT", "CONTROL", "CTRL", "DOWNARROW", "DOWN",
                 "LEFTARROW", "LEFT", "RIGHTARROW", "RIGHT", "UPARROW", "UP", "BREAK", "PAUSE", "CAPSLOCK", "DELETE",
                 "END",
                 "ESC", "ESCAPE", "HOME", "INSERT", "NUMLOCK", "PAGEUP", "PAGEDOWN", "PRINTSCREEN", "SCROLLLOCK",
                 "SPACE",
                 "TAB", "ENTER", " a", " b", " c", " d", " e", " f", " g", " h", " i", " j", " k", " l", " m", " n",
                 " o", " p", " q", " r", " s", " t",
                 " u", " v", " w", " x", " y", " z", " A", " B", " C", " D", " E", " F", " G", " H", " I", " J", " K",
                 " L", " M", " N", " O", " P",
                 " Q", " R", " S", " T", " U", " V", " W", " X", " Y", " Z", "F1", "F2", "F3", "F4", "F5", "F6", "F7",
                 "F8", "F9", "F10", "F11", "F12"]

keycodeCommands = [Keycode.WINDOWS, Keycode.GUI, Keycode.APPLICATION, Keycode.APPLICATION, Keycode.SHIFT, Keycode.ALT,
                   Keycode.CONTROL,
                   Keycode.CONTROL, Keycode.DOWN_ARROW, Keycode.DOWN_ARROW, Keycode.LEFT_ARROW, Keycode.LEFT_ARROW,
                   Keycode.RIGHT_ARROW, Keycode.RIGHT_ARROW,
                   Keycode.UP_ARROW, Keycode.UP_ARROW, Keycode.PAUSE, Keycode.PAUSE, Keycode.CAPS_LOCK, Keycode.DELETE,
                   Keycode.END, Keycode.ESCAPE,
                   Keycode.ESCAPE, Keycode.HOME, Keycode.INSERT, Keycode.KEYPAD_NUMLOCK, Keycode.PAGE_UP,
                   Keycode.PAGE_DOWN, Keycode.PRINT_SCREEN,
                   Keycode.SCROLL_LOCK, Keycode.SPACE, Keycode.TAB, Keycode.ENTER, Keycode.A, Keycode.B, Keycode.C,
                   Keycode.D, Keycode.E, Keycode.F, Keycode.G,
                   Keycode.H, Keycode.I, Keycode.J, Keycode.K, Keycode.L, Keycode.M, Keycode.N, Keycode.O, Keycode.P,
                   Keycode.Q, Keycode.R, Keycode.S, Keycode.T,
                   Keycode.U, Keycode.V, Keycode.W, Keycode.X, Keycode.Y, Keycode.Z, Keycode.A, Keycode.B, Keycode.C,
                   Keycode.D, Keycode.E, Keycode.F,
                   Keycode.G, Keycode.H, Keycode.I, Keycode.J, Keycode.K, Keycode.L, Keycode.M, Keycode.N, Keycode.O,
                   Keycode.P,
                   Keycode.Q, Keycode.R, Keycode.S, Keycode.T, Keycode.U, Keycode.V, Keycode.W, Keycode.X, Keycode.Y,
                   Keycode.Z,
                   Keycode.F1, Keycode.F2, Keycode.F3, Keycode.F4, Keycode.F5, Keycode.F6, Keycode.F7, Keycode.F8,
                   Keycode.F9,
                   Keycode.F10, Keycode.F11, Keycode.F12]


def convertLine(line):
    newline = []
    print(line)
    for j in range(len(keycodeCommands)):
        if line.find(duckyCommands[j]) != -1:
            newline.append(keycodeCommands[j])
    print(newline)
    return newline


def runScriptLine(line):
    for k in line:
        kbd.press(k)
    kbd.release_all()


def sendString(line):
    layout.write(line)


def parseLine(line):
    if (line[0:3] == "REM"):
        # ignore ducky script comments
        pass
    elif (line[0:5] == "DELAY"):
        time.sleep(float(line[6:]) / 1000)
    elif (line[0:6] == "STRING"):
        sendString(line[7:])
    elif (line[0:13] == "DEFAULT_DELAY"):
        defaultDelay = int(line[14:]) * 10
    elif (line[0:12] == "DEFAULTDELAY"):
        defaultDelay = int(line[13:]) * 10
    else:
        newScriptLine = convertLine(line)
        runScriptLine(newScriptLine)


kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# check GP0 for setup mode
# see setup mode for instructions
progStatus = False
progStatusPin = digitalio.DigitalInOut(GP0)
progStatusPin.switch_to_input(pull=digitalio.Pull.UP)
progStatus = not progStatusPin.value
defaultDelay = 0


def execute(duckyScriptPath, display):
    executing_splash = displayio.Group()
    display.show(executing_splash)
    text = label.Label(terminalio.FONT, text="Executing...", color=0xFF00FF, scale=3, x=15, y=60)
    executing_splash.append(text)

    f = open(duckyScriptPath, "r", encoding='utf-8')
    print("Running: " + duckyScriptPath)
    previousLine = ""
    duckyScript = f.readlines()
    for line in duckyScript:
        line = line.rstrip()
        if (line[0:6] == "REPEAT"):
            for i in range(int(line[7:])):
                # repeat the last command
                parseLine(previousLine)
                time.sleep(float(defaultDelay) / 1000)
        else:
            parseLine(line)
            previousLine = line
        time.sleep(float(defaultDelay) / 1000)

    executing_splash[0].x = 60
    executing_splash[0].text = "Done :)"
    time.sleep(1)
    print("Done")
