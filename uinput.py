import uinput
from time import sleep

with uinput.Device([uinput.KEY_A, uinput.KEY_D, uinput.KEY_SPACE]) as device:
    while True:
        device.emit_click(uinput.KEY_A)
        sleep(0.01)