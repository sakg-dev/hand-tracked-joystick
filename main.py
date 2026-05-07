import cv2
import time
import mediapipe as mp
from tools import draw_hand_landmarks, load_gesture_recognizer, line_intersection
from copy import deepcopy
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

    # For finding difference b/w rest and current ldm and do actions
    diff = None
    if (MAIN_HAND in handedness and len(rest_pose_ldms) > 0):
        main_hand_ldm = hlm[handedness.index(MAIN_HAND)]
        # diff = find_diff_between_ldms(rest_pose_ldms, main_hand_ldm)
        mhl = main_hand_ldm
        
        xa1 = mhl[12].x
        ya1 = mhl[12].y

        xa2 = mhl[0].x
        ya2 = mhl[0].y

        xb1 = mhl[4].x
        yb1 = mhl[4].y

        xb2 = mhl[20].x
        yb2 = mhl[20].y
        #line_intersection
        x, y = line_intersection(
            ((xa1, ya1), (xa2, ya2)),
            ((xb1, yb1), (xb2, yb2))
        )
        diff = deepcopy(mhl[0])
        diff.x = x
        diff.y = y

    result_img = draw_hand_landmarks(
        rgb_frame.numpy_view(), hlm, rest_pose_ldms, diff)
    cv2.imshow("img", result_img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()
