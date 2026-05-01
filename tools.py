import numpy as np
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision

def draw_hand_landmarks(rgb_img, result):
    annoted_img = np.copy(rgb_img)
    hand_landmarks_list = result.hand_landmarks

    for hand_landmarks in hand_landmarks_list:

        drawing_utils.draw_landmarks(
            image=annoted_img,
            landmark_list=hand_landmarks,
            connections=vision.HandLandmarksConnections.HAND_CONNECTIONS,
            landmark_drawing_spec=drawing_styles.get_default_hand_landmarks_style(),
            connection_drawing_spec=drawing_styles.get_default_hand_connections_style()
        )

    return annoted_img