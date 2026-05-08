from pynput.keyboard import Key, Controller
from time import sleep

keyboard = Controller()

while True:
    keyboard.press('a')
    keyboard.press('b')
    keyboard.press(Key.shift)
    sleep(2)
    keyboard.release('a')
    keyboard.release('b')
    keyboard.release(Key.shift)
    sleep(5)


