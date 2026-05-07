import cv2
import time
import mediapipe as mp
from tools import draw_hand_landmarks, load_gesture_recognizer, is_above_threshold
from copy import deepcopy
import uinput
# or use pynput

cam = cv2.VideoCapture(0)

# bundles both gesture recognizer and hand landmark tracker
gesture_recognizer = load_gesture_recognizer()

MAIN_HAND = "Right"
OFF_HAND = "Left"
LDM_SET_GESTURE = "Thumb_Up"
THRESHOLD = 0.05

rest_pose_ldms = []

pTime = 0
while True:
    with uinput.Device([uinput.KEY_A, uinput.KEY_D, uinput.KEY_SPACE, uinput.KEY_RIGHTSHIFT]) as device:
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

            if is_above_threshold(THRESHOLD, dx):
                if (dx > 0):
                    # print("+X") # left
                    print("A")
                    device.emit_click(uinput.KEY_A)
                else:
                    # print("-X") # right
                    print("D")
                    device.emit_click(uinput.KEY_D)
            if is_above_threshold(THRESHOLD, dy):
                if (dy > 0):
                    # print("+Y") # up
                    device.emit_click(uinput.KEY_SPACE)
                    print("Jump")
                else:
                    # print("-Y") # down
                    print("Snick")
                    device.emit_click(uinput.KEY_RIGHTSHIFT)

        result_img = draw_hand_landmarks(
            rgb_frame.numpy_view(), hlm, rest_pose_ldms)
        cv2.imshow("img", result_img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cam.release()
cv2.destroyAllWindows()
