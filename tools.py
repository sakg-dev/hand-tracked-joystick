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


def get_hand_connections_style(color):
    pass


def draw_hand_landmarks(rgb_img, hand_landmarks_list, rest_pose_ldms, diff):
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
    if diff:
        drawing_utils.draw_landmarks(
            image=annoted_img,
            landmark_list=[diff],
            landmark_drawing_spec=get_hand_landmarks_style((255, 0, 255))
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

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

# def find_diff_between_ldms(ldms1, ldms2): # rest_pose and main_hand_ldm
#     iss = False
#     val = None
#     if (len(ldms1) != 0 and len(ldms2) != 0):
#         # print(ldms2[0])
#         val = deepcopy(ldms2[0])
#         # val.x = ldms2[0].x - ldms2[12].x
#         val.y = ldms2[0].y - ldms2[12].y
#         print(val)
#         print(ldms2[0])
#         print(ldms2[12])
#         print("\n\n\n\n\n\n\n\n\n")

#     return val
