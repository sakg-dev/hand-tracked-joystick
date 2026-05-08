import cv2
import time
import mediapipe as mp
from tools import draw_hand_landmarks, load_gesture_recognizer, is_above_threshold
from copy import deepcopy
from pynput.keyboard import Key, Controller

cam = cv2.VideoCapture(0)

keyboard = Controller()

# bundles both gesture recognizer and hand landmark tracker
gesture_recognizer = load_gesture_recognizer()

MAIN_HAND = "Right"
OFF_HAND = "Left"
LDM_SET_GESTURE = "Thumb_Up"
THRESHOLD = 0.05

rest_pose_ldms = []

pTime = 0

prev_keys = []

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
    handedness = list(
        map(lambda handedness: handedness[0].category_name, handedness))

    # For setting rest pos
    if OFF_HAND in handedness:
        gesture = gestures[handedness.index(OFF_HAND)][0].category_name
        if (gesture == LDM_SET_GESTURE):
            try:
                rest_pose_ldms = hlm[handedness.index(
                    MAIN_HAND)]  # Main hand ldmks
            except:
                rest_pose_ldms = []
                print("Main hand not found")

    # For finding difference b/w rest and current ldms and do actions
    diff = None
    if (MAIN_HAND in handedness and len(rest_pose_ldms) > 0):
        main_hand_ldm = hlm[handedness.index(MAIN_HAND)]

        rest_pose_center = rest_pose_ldms[9]
        main_hand_center = main_hand_ldm[9]

        dx = rest_pose_center.x - main_hand_center.x
        dy = rest_pose_center.y - main_hand_center.y

        current_keys = []
        if is_above_threshold(THRESHOLD, dx):
            if (dx > 0):
                current_keys.append("A")
            else:
                current_keys.append("D")
        if is_above_threshold(THRESHOLD, dy):
            if (dy > 0):
                current_keys.append(Key.space)
            else:
                current_keys.append(Key.shift)

        if len(prev_keys) != 0:
            for key in list(set(prev_keys)-set(current_keys)): # release prev keys who are not in new
                keyboard.release(key)

        for key in current_keys:
            if key not in prev_keys: # if key is new then press it or else just let it be as it is already been pressed
                keyboard.press(key)

        prev_keys = current_keys
            

    result_img = draw_hand_landmarks(rgb_frame.numpy_view(), hlm, rest_pose_ldms)
    cv2.imshow("img", result_img)

    if cv2.waitKey(1) & 0xFF == 27:
        # later here clear everything before breaking the loop :)
        break

cam.release()
cv2.destroyAllWindows()
