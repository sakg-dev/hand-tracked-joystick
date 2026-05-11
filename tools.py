import numpy as np
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
import cv2
import random
from copy import deepcopy


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

    for hand_landmarks in hand_landmarks_list:
        drawing_utils.draw_landmarks(
            image=annoted_img,
            landmark_list=hand_landmarks,
            connections=vision.HandLandmarksConnections.HAND_CONNECTIONS,
            landmark_drawing_spec=drawing_styles.get_default_hand_landmarks_style(),
            connection_drawing_spec=drawing_styles.get_default_hand_connections_style()
        )

    if len(rest_pose_ldms) == 21:  # All parts of hand must be visible
        drawing_utils.draw_landmarks(
            image=annoted_img,
            landmark_list=rest_pose_ldms,
            connections=vision.HandLandmarksConnections.HAND_CONNECTIONS,
            landmark_drawing_spec=get_hand_landmarks_style((255, 0, 0)),
            connection_drawing_spec=drawing_styles.get_default_hand_connections_style()
        )

    annoted_img_bgr = cv2.cvtColor(annoted_img, cv2.COLOR_RGB2BGR)
    return annoted_img_bgr


def is_above_threshold(threshold, val):
    # ans = val > (-abs(threshold) if val < 0 else abs(threshold))
    return abs(val) > threshold


def quit_and_release(current_keys, keyboard):
    for key in current_keys:
        keyboard.release(key)
    return


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

