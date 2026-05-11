import cv2
import time
import numpy as np
import mediapipe as mp
from time import sleep
import threading
from tools import draw_hand_landmarks, load_gesture_recognizer, is_above_threshold, quit_and_release, randomize_int
from pynput.keyboard import Key, Controller as keyboard_controller
from pynput.mouse import Button, Controller as mouse_controller

cam = cv2.VideoCapture(0)

keyboard = keyboard_controller()
mouse = mouse_controller()

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
PINCH_DISTANCE = 6
H = 168
W = 224
CPS = 6
RIGHT_CPS = 3
CPS_MAX_RAND_FACTOR = 0.2

rest_pose_ldms = []

pTime = 0

prev_keys = []
prev_mouse_btn_type = None

def cps_loop(ms_per_click, btn):
    while True:
        # do task here
        # print("X")
        global cps_thread_running
        if cps_thread_running==False:
            break
        mouse.click(btn)
        sleep(randomize_int(ms_per_click, CPS_MAX_RAND_FACTOR)/1000)
    # print("thread is killed successfully")

cps_thread_running = False
cps_thread = None

while True:
    success, frame = cam.read()
    current_keys = []

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

    is_off_hand_palm_open = False

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
            quit_and_release(current_keys, keyboard)
            break
        elif gesture == "Open_Palm":
            is_off_hand_palm_open = True

    # For finding difference b/w rest and current ldms and do actions for keyboard
    if (MAIN_HAND in handedness and len(rest_pose_ldms) > 0):
        main_hand_ldm = hlm[handedness.index(MAIN_HAND)]

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

        # Vertical (0 and 9)
        rest_pose_diameter = rest_pose_ldms[0].y - rest_pose_ldms[17].y
        main_hand_diameter = main_hand_ldm[0].y - main_hand_ldm[17].y
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

    # For Mouse
    if (MAIN_HAND in handedness and len(rest_pose_ldms) > 0):
        def hold_press(btn):
            mouse.press(btn)
        def hold_release(btn):
            mouse.release(btn)
        def cps_start(btn):
            global cps_thread_running
            global cps_thread
            cps_thread_running = True
            cps = CPS if is_off_hand_palm_open == False else RIGHT_CPS
            cps_thread = threading.Thread(target=cps_loop,args=[int(1000/cps), btn])
            cps_thread.start()
        def cps_end():
            global cps_thread_running
            global cps_thread 
            cps_thread_running = False
            cps_thread.join()
        
        main_hand_ldms = hlm[handedness.index(MAIN_HAND)]

        thumb = main_hand_ldms[4]
        index = main_hand_ldms[8]
        middle = main_hand_ldms[12]

        thumb_x, thumb_y = int(thumb.x*W), int(thumb.y*H)
        index_x, index_y = int(index.x*W), int(index.y*H)
        middle_x, middle_y = int(middle.x*W), int(middle.y*H)

        thumb_and_index_distance = cv2.norm(
            (thumb_x, thumb_y), (index_x, index_y)
        )
        thumb_and_middle_distance = cv2.norm(
            (thumb_x, thumb_y), (middle_x, middle_y)
        )

        thumb_and_index_pinch = thumb_and_index_distance <= PINCH_DISTANCE
        thumb_and_middle_pinch = thumb_and_middle_distance <= PINCH_DISTANCE


        if(thumb_and_index_pinch and thumb_and_middle_pinch):
            print("User can't do both types of click at same time")
        else:
            current_mouse_btn_type = None
            if thumb_and_middle_pinch:
                current_mouse_btn_type = "hold"
            elif thumb_and_index_pinch:
                current_mouse_btn_type = "high_cps"

            # If prev btn exist but now it doesn't, release prev
            # If current btn exist but prev is null press btn but if prev is not null but different so relase prev and press current
            btn = Button.left if is_off_hand_palm_open == False else Button.right
            if prev_mouse_btn_type:
                if not current_mouse_btn_type:
                    if prev_mouse_btn_type=="hold":
                        hold_release(btn)
                    elif prev_mouse_btn_type == "high_cps":
                        cps_end()
                else:
                    if prev_mouse_btn_type != current_mouse_btn_type:
                        if prev_mouse_btn_type=="hold":
                            hold_release(btn)
                        elif prev_mouse_btn_type=="high_cps":
                            cps_end()

                        if current_mouse_btn_type == "hold":
                            hold_press(btn)
                        elif current_mouse_btn_type=="high_cps":
                            cps_start(btn)
            else:
                if current_mouse_btn_type:
                    if current_mouse_btn_type=="hold":
                        hold_press(btn)
                    elif current_mouse_btn_type=="high_cps":
                        cps_start(btn)


            prev_mouse_btn_type = current_mouse_btn_type

    result_img = draw_hand_landmarks(
        rgb_frame.numpy_view(), hlm, rest_pose_ldms)
    # Either do width and height or fx and fy - one thing only
    resized_result_img = cv2.resize(
        result_img, None, fx=RESIZE_FX, fy=RESIZE_FY)
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE | cv2.WINDOW_GUI_NORMAL)
    cv2.imshow(WIN_NAME, resized_result_img)

    if cv2.waitKey(1) & 0xFF == 27:
        # later here clear everything before breaking the loop :)
        quit_and_release(current_keys, keyboard)
        break

cam.release()
cv2.destroyAllWindows()