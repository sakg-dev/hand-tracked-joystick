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

# import sys
# sys.path.insert(0, "/home/sakg/Desktop/hand_tracked_joystick/")
# from core.gesture_recognizer import Gesture_recognizer
# gest = Gesture_recognizer()

# isit = True
# if isit:
#     a = 6
# print(a)

# from time import time, sleep
# import random
# prev = time()
# randomized_millisec = random.randint(500,1000)
# sleep(randomized_millisec/1000)
# current = time()
# print(round(current-prev,2))

# a = ["abc","def","ghl"]
# b = ["ghl","def","pqy"]
# print(list(set(a).intersection(b)))
# print(list(set(a) - set(b)))

# a = {
#     "a":None,
#     "b":"Hi"
# }
# print(None in list(a.values()))