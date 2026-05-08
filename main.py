import cv2
import time
import numpy as np
import mediapipe as mp
from tools import draw_hand_landmarks, load_gesture_recognizer, is_above_threshold
from pynput.keyboard import Key, Controller

cam = cv2.VideoCapture(0)

keyboard = Controller()

# bundles both gesture recognizer and hand landmark tracker
gesture_recognizer = load_gesture_recognizer()

MAIN_HAND = "Left"
OFF_HAND = "Right"
LDM_SET_GESTURE = "Thumb_Up"
QUIT_GESTURE = "Thumb_Down"
WIN_NAME = "gameee"
THRESHOLD = 0.05
RESIZE_FX = 0.35
RESIZE_FY = 0.35

rest_pose_ldms = []

pTime = 0

prev_keys = []

while True:
    success, frame = cam.read()

    cTime = time.time()
    fps = round(1/(cTime-pTime))
    pTime = cTime
    flipped_frame = cv2.flip(frame, 1)
    img_with_fps = cv2.putText(flipped_frame, str(
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
        elif gesture == QUIT_GESTURE:
            quit()
            break

    # For finding difference b/w rest and current ldms and do actions
    diff = None
    if (MAIN_HAND in handedness and len(rest_pose_ldms) > 0):
        main_hand_ldm = hlm[handedness.index(MAIN_HAND)]
        current_keys = []

        rest_pose_center = rest_pose_ldms[9]
        main_hand_center = main_hand_ldm[9]
        dx = rest_pose_center.x - main_hand_center.x
        dy = rest_pose_center.y - main_hand_center.y
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

        # Horizontal(4 and 20)
        # rest_pose_diameter = rest_pose_ldms[20].x - rest_pose_ldms[4].x
        # main_hand_diameter = main_hand_ldm[20].x - main_hand_ldm[4].x

        # Vertical (0 and 12)
        rest_pose_diameter = rest_pose_ldms[0].y - rest_pose_ldms[12].y
        main_hand_diameter = main_hand_ldm[0].y - main_hand_ldm[12].y
        dz = rest_pose_diameter - main_hand_diameter

        # print(dz) # negative = forward, positive = backward

        if is_above_threshold(0.01, dz):
            if (dz > 0):
                current_keys.append("S")
            else:
                current_keys.append("W")

        if len(prev_keys) != 0:
            # release prev keys who are not in new
            for key in list(set(prev_keys)-set(current_keys)):
                keyboard.release(key)

        for key in current_keys:
            if key not in prev_keys:  # if key is new then press it or else just let it be as it is already been pressed
                keyboard.press(key)

        prev_keys = current_keys

    result_img = draw_hand_landmarks(
        rgb_frame.numpy_view(), hlm, rest_pose_ldms)
    resized_result_img = cv2.resize(result_img, None, fx=RESIZE_FX, fy=RESIZE_FY)
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE | cv2.WINDOW_GUI_NORMAL)
    cv2.imshow(WIN_NAME, resized_result_img)

    if cv2.waitKey(1) & 0xFF == 27:
        # later here clear everything before breaking the loop :)
        quit()
        break

cam.release()
cv2.destroyAllWindows()
