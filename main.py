import cv2
import time
import mediapipe as mp
from tools import draw_hand_landmarks, load_gesture_recognizer
# import uinput
# or use pynput

cam = cv2.VideoCapture(0)

# bundles both gesture recognizer and hand landmark tracker
gesture_recognizer = load_gesture_recognizer()

MAIN_HAND = "Right"
OFF_HAND = "Left"
LDM_SET_GESTURE = "Thumb_Up"

rest_pose_ldms = []

pTime = 0
while True:
    success, frame = cam.read()

    cTime = time.time()
    fps = round(1/(cTime-pTime))
    pTime = cTime
    img_with_fps = cv2.putText(frame, str(
        fps), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 100, 255), 2)

    rgb_img = cv2.cvtColor(img_with_fps, cv2.COLOR_BGR2RGB)
    rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)

    r = gesture_recognizer.recognize(rgb_frame)
    gestures, handedness, hlm, hwlm = r.gestures, r.handedness, r.hand_landmarks, r.hand_world_landmarks

    # glitches and shows wrong arr when new item is added or removed even after adding check of score hence need some kind of cooldown ig!
    # if handedness[0].score>0.95 else False
    handedness = list(map(lambda handedness: handedness[0].category_name, handedness))

    if OFF_HAND in handedness:
        gesture = gestures[handedness.index(OFF_HAND)][0].category_name
        if(gesture==LDM_SET_GESTURE):
            try:
                rest_pose_ldms = hlm[handedness.index(MAIN_HAND)] # Main hand ldmks
            except:
                rest_pose_ldms = []
                print("Main hand not found")

    result_img = draw_hand_landmarks(rgb_frame.numpy_view(), hlm, rest_pose_ldms)
    cv2.imshow("img", result_img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()
