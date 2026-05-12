import os
import sys
path = os.path.abspath(".")
sys.path.insert(0, path)
from tools import quit_and_release, is_above_threshold
from config.constants import OFF_HAND, MAIN_HAND, LDM_SET_GESTURE, QUIT_GESTURE, RIGHT_CLICK_GESTURE, LANDMARK_DELTA_THRESHOLD, WINDOW_WIDTH, WINDOW_HEIGHT, PINCH_THRESHOLD
import cv2
from pynput.keyboard import Key

class Gesture_mapper:
    """Takes Hand landmarks and outputs all actions that has to be taken."""

    def __init__(self):
        self.rest_pose_ldms = []

    def _off_hand_gesture_actions(self, action_taker):
        handedness = self.handedness

        if OFF_HAND not in handedness:
            return

        gesture = self.gestures[handedness.index(OFF_HAND)][0].category_name

        if (gesture == LDM_SET_GESTURE):
            try:
                self.rest_pose_ldms = self.hlm[handedness.index(MAIN_HAND)]
            except:
                self.rest_pose_ldms = []
                print("Main hand not found")
        elif gesture == QUIT_GESTURE:
            print(action_taker.prev_mouse_btn_type,end="\n\n\n\n")
            quit_and_release(action_taker.prev_keys, action_taker.prev_mouse_btn_type, action_taker._cps_end)
        elif gesture == RIGHT_CLICK_GESTURE:
            self.is_off_hand_palm_open = True

    def _main_hand_gesture_actions(self):
        handedness = self.handedness
        rest_pose_ldms = self.rest_pose_ldms
        if (MAIN_HAND not in handedness or len(rest_pose_ldms) == 0):
            return

        main_hand_ldm = self.hlm[handedness.index(MAIN_HAND)]

        # ---------Keyboard------------------
        rest_pose_center = rest_pose_ldms[9]
        main_hand_center = main_hand_ldm[9]
        dx = rest_pose_center.x - main_hand_center.x
        dy = rest_pose_center.y - main_hand_center.y
        if is_above_threshold(LANDMARK_DELTA_THRESHOLD, dx):
            if (dx > 0):
                self.current_keys.append("A")
            else:
                self.current_keys.append("D")
        if is_above_threshold(LANDMARK_DELTA_THRESHOLD, dy):
            if (dy > 0):
                self.current_keys.append(Key.space)
            else:
                self.current_keys.append(Key.shift)

        rest_pose_diameter = rest_pose_ldms[0].y - rest_pose_ldms[17].y
        main_hand_diameter = main_hand_ldm[0].y - main_hand_ldm[17].y
        dz = rest_pose_diameter - main_hand_diameter
        if is_above_threshold(0.01, dz):
            if (dz > 0):
                self.current_keys.append("S")
            else:
                self.current_keys.append("W")

        # ---------Mouse--------------------
        thumb = main_hand_ldm[4]
        index = main_hand_ldm[8]
        middle = main_hand_ldm[12]

        thumb_x, thumb_y = int(
            thumb.x*WINDOW_WIDTH), int(thumb.y*WINDOW_HEIGHT)
        index_x, index_y = int(
            index.x*WINDOW_WIDTH), int(index.y*WINDOW_HEIGHT)
        middle_x, middle_y = int(
            middle.x*WINDOW_WIDTH), int(middle.y*WINDOW_HEIGHT)

        thumb_and_index_distance = cv2.norm(
            (thumb_x, thumb_y), (index_x, index_y)
        )
        thumb_and_middle_distance = cv2.norm(
            (thumb_x, thumb_y), (middle_x, middle_y)
        )

        thumb_and_index_pinch = thumb_and_index_distance <= PINCH_THRESHOLD
        thumb_and_middle_pinch = thumb_and_middle_distance <= PINCH_THRESHOLD

        if (thumb_and_index_pinch and thumb_and_middle_pinch):
            print("User can't do both types of click at same time")
        else:
            if thumb_and_middle_pinch:
                self.current_mouse_btn_type = "hold"
            elif thumb_and_index_pinch:
                self.current_mouse_btn_type = "high_cps"

    def map(self, hlm, handedness, gestures, action_taker):
        self.hlm = hlm
        self.handedness = list(map(lambda hd: hd[0].category_name, handedness))
        self.gestures = gestures

        self.is_off_hand_palm_open = False
        self.current_keys = []
        self.current_mouse_btn_type = None

        if len(self.handedness) == 0:
            return False

        self._off_hand_gesture_actions(action_taker)

        self._main_hand_gesture_actions()

        return [self.current_keys, self.current_mouse_btn_type, self.is_off_hand_palm_open, self.rest_pose_ldms]
