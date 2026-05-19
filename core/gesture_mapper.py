import os
import sys
path = os.path.abspath(".")
sys.path.insert(0, path)
from tools import quit_and_release, is_above_threshold
from config.constants import OFF_HAND, MAIN_HAND, LDM_SET_GESTURE, QUIT_GESTURE, RIGHT_CLICK_GESTURE, LANDMARK_DELTA_THRESHOLD, WINDOW_WIDTH, WINDOW_HEIGHT, PINCH_THRESHOLD
import cv2
from pynput.keyboard import Key
import time


class Gesture_mapper:
    """Takes Hand landmarks and outputs all actions that has to be taken."""

    def __init__(self):
        self.rest_pose_ldms = []
        self.last_forward_time = None
        self.last_horizontal_move_for_invtentory = {"time": None, "side": None}
        self.last_rest_pose_time = None
        self.sprint = False

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
            quit_and_release(
                action_taker.prev_keys, action_taker.prev_mouse_btn_types, action_taker._cps_end)
        elif gesture == RIGHT_CLICK_GESTURE:
            self.is_off_hand_palm_open = True

    def _main_hand_gesture_actions(self):
        handedness = self.handedness
        rest_pose_ldms = self.rest_pose_ldms
        if (MAIN_HAND not in handedness or len(rest_pose_ldms) == 0):
            return

        main_hand_ldm = self.hlm[handedness.index(MAIN_HAND)]
        current_time = time.time()

        # ---------Keyboard------------------
        rest_pose_center = rest_pose_ldms[9]
        main_hand_center = main_hand_ldm[9]
        dx = rest_pose_center.x - main_hand_center.x
        dy = rest_pose_center.y - main_hand_center.y
        if is_above_threshold(LANDMARK_DELTA_THRESHOLD, dx):
            current_side = "A" if dx > 0 else "D"
            if abs(dx) < 0.1:
                self.current_keys.append(Key.scroll_lock) # Pressing a useless key to make it busy..
                lst_x_move = self.last_horizontal_move_for_invtentory
                if None not in list(lst_x_move.values()): # values complete
                    if lst_x_move["side"] == current_side and (current_time - lst_x_move["time"]) < 0.5:
                        pass
                    else:
                        # print("tim ran out or diff side")
                        self.last_horizontal_move_for_invtentory = {
                            "side": current_side,
                            "time": current_time
                        }
                else:
                    self.last_horizontal_move_for_invtentory = {
                        "side": current_side,
                        "time": current_time
                    }
            else:
                self.current_keys.append(current_side)
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

                if self.last_forward_time and self.last_rest_pose_time:
                    if (current_time - self.last_forward_time) < 1 and current_time > self.last_rest_pose_time > self.last_forward_time:
                        self.last_forward_time = None
                        # Sprint must start when W and sprint is true and stop when its w is stopped
                        self.sprint = True
                    else:
                        self.last_forward_time = time.time()
                else:
                    self.last_forward_time = time.time()

        if self.sprint:
            if "W" in self.current_keys:
                self.current_keys.append("R")
            else:
                self.sprint = False

        if len(self.current_keys) == 0 and len(self.current_mouse_btn_types) == 0: # both keyboards and mouse
            lst_x_move = self.last_horizontal_move_for_invtentory
            if self.last_rest_pose_time and None not in list(lst_x_move.values()):
                if current_time - self.last_rest_pose_time<1 and current_time > lst_x_move["time"] > self.last_rest_pose_time:
                    self.current_mouse_btn_types.append("prev_inventory" if lst_x_move["side"]=="A" else "next_inventory")
            self.last_rest_pose_time = current_time

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
                self.current_mouse_btn_types.append("hold")
            elif thumb_and_index_pinch:
                self.current_mouse_btn_types.append("high_cps")

    def map(self, hlm, handedness, gestures, action_taker):
        self.hlm = hlm
        self.handedness = list(map(lambda hd: hd[0].category_name, handedness))
        self.gestures = gestures

        self.is_off_hand_palm_open = False
        self.current_keys = []
        self.current_mouse_btn_types = []

        if len(self.handedness) == 0:
            return False

        self._off_hand_gesture_actions(action_taker)

        self._main_hand_gesture_actions()

        return [self.current_keys, self.current_mouse_btn_types, self.is_off_hand_palm_open, self.rest_pose_ldms]
