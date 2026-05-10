import cv2
import sys
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python.vision import drawing_styles, drawing_utils
from mediapipe.tasks.python import vision

sys.path.insert(0, "/home/sakg/Desktop/hand_tracked_joystick/")
from tools import load_gesture_recognizer

cam = cv2.VideoCapture(0)
gesture_recognizer = load_gesture_recognizer()

H = 480
W = 640


def draw_hand_landmarks(rgb_img, hand_landmarks_list):
    annoted_img = np.copy(rgb_img)

    for hand_landmarks in hand_landmarks_list:
        drawing_utils.draw_landmarks(
            image=annoted_img,
            landmark_list=hand_landmarks,
            connections=vision.HandLandmarksConnections.HAND_CONNECTIONS,
            landmark_drawing_spec=drawing_styles.get_default_hand_landmarks_style(),
            connection_drawing_spec=drawing_styles.get_default_hand_connections_style()
        )

    annoted_img_bgr = cv2.cvtColor(annoted_img, cv2.COLOR_RGB2BGR)
    return annoted_img_bgr


while True:
    success, frame = cam.read()

    rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)

    r = gesture_recognizer.recognize(rgb_frame)
    gestures, handedness, hlm, hwlm = r.gestures, r.handedness, r.hand_landmarks, r.hand_world_landmarks

    final_img = draw_hand_landmarks(rgb_frame.numpy_view(), hlm)

    if len(hlm) > 0:
        thumb = hlm[0][4]
        index = hlm[0][8]
        x1, y1 = int(thumb.x*W), int(thumb.y*H)
        x2, y2 = int(index.x*W), int(index.y*H)
        cv2.line(final_img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        print(cv2.norm((x1,y1),(x2,y2))) # Getting

    cv2.imshow("frame", final_img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()
