import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
import cv2
from math import atan2, degrees

cam = cv2.VideoCapture(0)

base_options = python.BaseOptions(
    model_asset_path="./models/gesture_recognizer.task"
)

options = vision.GestureRecognizerOptions(
    base_options=base_options,
    num_hands=2
)
GestureRecognizer = vision.GestureRecognizer.create_from_options(options)

while True:
    success, frame = cam.read()

    flipped_frame = cv2.flip(frame, 1)

    rgb_frame = mp.Image(
        mp.ImageFormat.SRGB,
        cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
    )

    r = GestureRecognizer.recognize(rgb_frame)
    gestures, handedness, hlm, hwlm = r.gestures, r.handedness, r.hand_landmarks, r.hand_world_landmarks
    print(handedness)

    if len(hlm) > 0:
        lms = hlm[0]
        # wrist, m_finger = lms[0], lms[9]
        # print(wrist)
        # print(middle_finger_mcp,end="\n\n\n\n")
        # angle = degrees(atan2(m_finger.y - wrist.y, m_finger.x - wrist.x))
        pinky, wrist = lms[17], lms[0]
        

    cv2.imshow("img", flipped_frame)

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()
