import numpy as np
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision
import cv2
import random
from copy import deepcopy
from pynput.keyboard import Controller as kController
from pynput.mouse import Button, Controller as mController


def get_hand_landmarks_style(color):
    _hand_ldm_style = deepcopy(drawing_styles._HAND_LANDMARK_STYLE)
    hand_ldm_style = {}
    for k, v in _hand_ldm_style.items():
        for ldm in k:
            v.color = color
            hand_ldm_style[ldm] = v
    return hand_ldm_style


def draw_hand_landmarks(rgb_img, hand_landmarks_list, rest_pose_ldms):
    annoted_img = np.copy(rgb_img)

    if len(rest_pose_ldms) > 0:  # All parts of hand must be visible
        drawing_utils.draw_landmarks(
            image=annoted_img,
            landmark_list=rest_pose_ldms,
            landmark_drawing_spec=get_hand_landmarks_style((255, 0, 0))
        )

    annoted_img_bgr = cv2.cvtColor(annoted_img, cv2.COLOR_RGB2BGR)
    return annoted_img_bgr


def is_above_threshold(threshold, val):
    # ans = val > (-abs(threshold) if val < 0 else abs(threshold))
    return abs(val) > threshold


def quit_and_release(keys, prev_mouse_btn_types, _cps_end):
    keyboard = kController()
    for key in keys:
        keyboard.release(key)
    
    # Mouse: Simple left and right press/release || high cps loop
    # Rn user will never do right click b4 releasing as we need to keep palm open of off hand for right click but for closing we need to do down thumbsup, it means we have to check for left hold click and high cps
    mouse = mController()
    if "hold" in prev_mouse_btn_types:
        mouse.release(Button.left)
    if "high_cps" in prev_mouse_btn_types:
        _cps_end()

    raise RuntimeError("Quitting")


def randomize_int(val, max_factor):
    rand_factor = round(random.uniform(0, max_factor), 2)
    rand_no = int(val*rand_factor)
    rand_sign = random.randint(0, 1)
    rand_val = None
    if rand_sign > 0:
        rand_val = val + rand_no
    else:
        rand_val = val - rand_no
    return rand_val

