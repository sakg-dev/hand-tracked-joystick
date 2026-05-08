from pynput.keyboard import Key, Controller
from time import sleep

keyboard = Controller()

while True:
    keyboard.press('a')
    sleep(2)
    keyboard.release('a')
    sleep(5)


