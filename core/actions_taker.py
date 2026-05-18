import os
import sys
path = os.path.abspath(".")
sys.path.insert(0, path)
from tools import randomize_int
from config.constants import LEFT_CPS, RIGHT_CPS, CPS_MAX_RAND_FACTOR
from pynput.keyboard import Controller as kController
from pynput.mouse import Button, Controller as mController
from time import sleep
import threading


class Action_taker:
    def __init__(self):
        self.keyboard = kController()
        self.mouse = mController()

        self.prev_keys = []
        self.prev_mouse_btn_types = []
        self.cps_thread_running = False
        self.cps_thread = None

    def _keyboard(self):
        prev_keys = self.prev_keys
        current_keys = self.current_keys

        if len(prev_keys) != 0:
            # release prev keys who are not in new
            for key in list(set(prev_keys)-set(current_keys)):
                self.keyboard.release(key)

        for key in current_keys:
            if key not in prev_keys:  # if key is new then press it or else just let it be as it is already been pressed
                self.keyboard.press(key)

        self.prev_keys = current_keys

    def _cps_loop(self, ms_per_click, btn):
        while True:
            if self.cps_thread_running == False:
                break
            self.mouse.click(btn)
            sleep(randomize_int(ms_per_click, CPS_MAX_RAND_FACTOR)/1000)

    def _hold_press(self, btn):
        self.mouse.press(btn)

    def _hold_release(self, btn):
        self.mouse.release(btn)

    def _cps_start(self, btn):
        self.cps_thread_running = True
        cps = LEFT_CPS if self.is_off_hand_palm_open == False else RIGHT_CPS
        self.cps_thread = threading.Thread(
            target=self._cps_loop, args=[int(1000/cps), btn])
        self.cps_thread.start()

    def _cps_end(self):
        self.cps_thread_running = False
        self.cps_thread.join()

    def _mouse(self):
        btn = Button.left if self.is_off_hand_palm_open == False else Button.right
        prev_mouse_btn_types = self.prev_mouse_btn_types
        current_mouse_btn_types = self.current_mouse_btn_types

        if len(current_mouse_btn_types) == 0:
            if len(prev_mouse_btn_types) > 0:
                if "hold" in prev_mouse_btn_types:
                    self._hold_release(btn)
                if "high_cps" in prev_mouse_btn_types:
                    self._cps_end()
        else:
            not_anymore_key_types = list(set(prev_mouse_btn_types) - set(current_mouse_btn_types))
            if len(not_anymore_key_types) != 0:
                if "hold" in not_anymore_key_types:
                    self._hold_release(btn)
                if "high_cps" in not_anymore_key_types:
                    self._cps_end()

            new_key_types = list(set(current_mouse_btn_types) - set(prev_mouse_btn_types))
            if "hold" in new_key_types:
                self._hold_press(btn)
            if "high_cps" in new_key_types:
                self._cps_start(btn)
        self.prev_mouse_btn_types = current_mouse_btn_types

    def take_action(self, current_keys, current_mouse_btn_types, is_off_hand_palm_open):
        self.current_keys = current_keys
        self.is_off_hand_palm_open = is_off_hand_palm_open
        self.current_mouse_btn_types = current_mouse_btn_types

        self._keyboard()
        self._mouse()
