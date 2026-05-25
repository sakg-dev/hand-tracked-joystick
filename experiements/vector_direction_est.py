import os
import sys
path = os.path.abspath(".")
sys.path.insert(0, path)
from tools import draw_hand_landmarks
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
import numpy as np
import cv2
import random

cam = cv2.VideoCapture(0)

base_options = python.BaseOptions(
    model_asset_path="./models/gesture_recognizer.task"
)
options = vision.GestureRecognizerOptions(
    base_options=base_options,
    num_hands=2
)
GestureRecognizer = vision.GestureRecognizer.create_from_options(options)

# Constants
MAIN_HAND = "Right"
OFF_HAND="Left"
SET_REST_POSE_GESTURE = "Thumb_Up"

# Vars
rest_pose_ldms = []

while True:
    success, frame = cam.read()

    # flipped_frame = cv2.flip(frame, 1)
    flipped_frame = frame # for laptop

    rgb_frame = mp.Image(
        mp.ImageFormat.SRGB,
        cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
    )

    r = GestureRecognizer.recognize(rgb_frame)
    gestures, handedness, hlm, hwlm = r.gestures, r.handedness, r.hand_landmarks, r.hand_world_landmarks
    handedness = list(map(lambda h:h[0].category_name, handedness))

    # if OFF_HAND in handedness:
    #     idx = handedness.index(OFF_HAND)
    #     gesture = gestures[idx][0].category_name

    #     if gesture == SET_REST_POSE_GESTURE:
    #         # print("Set rest pose")
    #         if MAIN_HAND in handedness:
    #             rest_pose_ldms = hlm[handedness.index(MAIN_HAND)]

    new_ldm = None
    if len(hwlm) > 0: # and len(rest_pose_ldms) == 21
        wlms = hwlm[0]
        lms = hlm[0]
        points = np.asarray([
                [wlms[0].x,wlms[0].y,wlms[0].z], 
                [wlms[5].x,wlms[5].y,wlms[5].z], 
                [wlms[17].x,wlms[17].y,wlms[17].z]
            ],
            dtype=np.float32
        )
        normal_vector = np.cross(points[2] - points[0], points[1] - points[2])
        if MAIN_HAND in handedness:
            normal_vector *= -1
        normal_vector /= np.linalg.norm(normal_vector)
        new_ldm = mp.tasks.components.containers.NormalizedLandmark()
        new_ldm.x, new_ldm.y, new_ldm.z = list(map(lambda num:num.item(), normal_vector))
        rest_pose_ldms = [lms[9], new_ldm]
        x,y = new_ldm.x, new_ldm.y
        if y < -0.3:
            print("up")
        elif y > 0.4:
            print("down")
        if x > 0.8:
            print("left")
        elif x < 0.2:
            print("right")

        # Finding perpendicular of line, and finding the rotatiion by that 
        # if MAIN_HAND in handedness:
        #     lms = hlm[handedness.index(MAIN_HAND)]
        #     pinky, wrist = lms[17], lms[0]
        #     dx = pinky.x - wrist.x
        #     dy = pinky.y - wrist.y
        #         # "left": (-dy, dx),
        #         # "right": (dy, -dx)
        #     perpendicular_ldm_left = mp.tasks.components.containers.NormalizedLandmark()
        #     perpendicular_ldm_left.x = -dy
        #     perpendicular_ldm_left.y = dx
        #     perpendicular_ldm_left.z = (pinky.z + wrist.z) / 2
        #     rest_pose_ldms = [perpendicular_ldm_left]
            
        # top/bottom working well but left/right is also getting active on top/bottom, need other ldms..
        # lms = hlm[0]
        # pinky, middle_finger_mcp = round(lms[20].z,4), round(lms[9].z,4)
        # rest_pinky, rest_middle_finger_mcp = round(rest_pose_ldms[20].z,4), round(rest_pose_ldms[9].z,4)
        # if abs(rest_middle_finger_mcp -  middle_finger_mcp) > 0.02:
        #     print("top/bottom")
        # print(abs(rest_pinky -  pinky))
        # if abs(rest_pinky -  pinky) > 0.03:
        #     print("left/right",end = "\n" * random.randint(1,3))
        # print(abs(rest_middle_finger_mcp -  middle_finger_mcp))
        # print(abs(rest_pinky -  pinky))
        # print("\n\n\n\n\n")

        # lms = hlm[0]
        # pinky, wrist = lms[17], lms[0]
        # rest_pinky,rest_wrist = rest_pose_ldms[17], rest_pose_ldms[0]
        # pinky_diff = round(rest_pinky.z - pinky.z, 3)
        # wrist_diff = round((rest_wrist.z - wrist.z)*100000, 3)
        # rand = "\n" * random.randint(1,3)
        # if abs(wrist_diff) > 0.01:
        #     print("Top and Bottom",end=rand)
        # else:
        #     if abs(pinky_diff) > 0.01:
        #         print("Left and right",end=rand)

    result_img = draw_hand_landmarks(rgb_frame.numpy_view(), hlm, rest_pose_ldms)
    if new_ldm:
        img_size = result_img.shape
        h,w,_a = img_size
        cv2.line(result_img, (int((new_ldm.x)*w),int((new_ldm.y)*h)), (int((hlm[0][9].x)*w),int((hlm[0][9].y)*h)),(255,0,0))
    cv2.imshow("img", result_img)

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()
