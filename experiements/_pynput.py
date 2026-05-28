# from pynput.keyboard import Key, Controller as kController
# from pynput.mouse import Button, Controller as mController
# from time import sleep
# import random

# keyboard = kController()
# mouse = mController()

# while True:
    # print("pressing")
    # keyboard.press('a')
    # keyboard.release('a')
    # keyboard.press('b')
    # keyboard.press(Key.shift)
    # sleep(0.2)
    # keyboard.release('b')
    # keyboard.release(Key.shift)
    # sleep(5)

# sleep(5)
# while True:
#     sleep(0.1) # 90 cps lol
#     mouse.click(Button.left)
#     mouse.release(Button.right)
#     keyboard.release("W")
#     keyboard.release("A")
#     keyboard.release("S")
#     keyboard.release("D")
#     keyboard.release(Key.shift)
#     keyboard.release(Key.space)


# sleep(5)
# info = {
#     "time": 0,
#     "for": "left"
# }
# for_list = ["left", "right", "top", "bottom"]
# val = 5
# while True:
#     if info["time"] < 300:
#         for_val = info["for"]
#         x = 0
#         y = 0
#         if for_val == "left":
#             x = -val
#         elif for_val == "right":
#             x = val
#         if for_val == "top":
#             y = -val
#         elif for_val == "bottom":
#             y = val
#         mouse.move(x, y)
#         sleep(0.01)
#         info["time"] += 1
#     else:
#         new_move = for_list[random.randint(0, len(for_list)-1)]
#         info = {
#             "time": 0,
#             "for": new_move
#         }
