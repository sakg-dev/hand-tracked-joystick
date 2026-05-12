from pynput.keyboard import Key, Controller as kController
from pynput.mouse import Button, Controller as mController
from time import sleep

keyboard = kController()
mouse = mController()

# while True:
#     keyboard.press('a')
#     keyboard.press('b')
#     keyboard.press(Key.shift)
#     sleep(2)
#     keyboard.release('a')
#     keyboard.release('b')
#     keyboard.release(Key.shift)
#     sleep(5)

sleep(5)
while True:
    sleep(1) # 90 cps lol
    mouse.release(Button.left)
    mouse.release(Button.right)
    keyboard.release("W")
    keyboard.release("A")
    keyboard.release("S")
    keyboard.release("D")
    keyboard.release(Key.shift)
    keyboard.release(Key.space)