import numpy as np
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
import cv2
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


def load_gesture_recognizer():
    base_option = python.BaseOptions(
        model_asset_path="models/gesture_recognizer.task")
    options = vision.GestureRecognizerOptions(
        base_options=base_option,
        num_hands=2
    )
    recognizer = vision.GestureRecognizer.create_from_options(options)
    return recognizer
