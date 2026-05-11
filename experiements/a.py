# import random
# val = int(1000/6)
# rand_factor = random.randint(0, 20)/100
# rand_no = int(val*rand_factor)
# rand_sign = random.randint(0, 1)
# rand_val = None
# if rand_sign > 0:
#     rand_val = val + rand_no
# else:
#     rand_val = val - rand_no
# print(rand_val)


# import random
# print(round(random.uniform(0, 0.2), 2))


# while True:
#     if(some_condition_is_true):
#         start_the_loop()
#     elif(another_condition_is_true):
#         end_the_loop()
#     else:
#         print("Nothing happened")


# import threading

# import cv2
# cam = cv2.VideoCapture(0)
# print(cam.isOpened())

import sys
sys.path.insert(0, "/home/sakg/Desktop/hand_tracked_joystick/")
from core.gesture_recognizer import Gesture_recognizer
gest = Gesture_recognizer()