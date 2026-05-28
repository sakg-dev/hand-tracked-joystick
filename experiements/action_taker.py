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
        self.thread_tasks = []
        self.prev_thread_tasks = []
    
    def _thread_work(self):
        tasks = self.thread_tasks
        if len(tasks) > 0:
            for task in tasks:
                task_name, func, args = task["task_name"], task["func"], task["args"]
                if task_name not in self.prev_thread_tasks:
                    func(args)
            self.prev_thread_tasks = list(map(lambda t: t["task_name"], tasks))
        else:
            self.prev_thread_tasks = []
            # task_name, 
            # if 


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
            self.mouse.click(btn)
            sleep(randomize_int(ms_per_click, CPS_MAX_RAND_FACTOR)/1000)

    def _hold_press(self, btn):
        self.mouse.press(btn)

    def _hold_release(self, btn):
        self.mouse.release(btn)

    def _cps_start(self, btn):
        cps = LEFT_CPS if self.is_off_hand_palm_open == False else RIGHT_CPS
        self.thread_tasks.append({
            "task_name": "cps",
            "func": self._cps_loop,
            "args": [int(1000/cps), btn]
        })

    def _cps_end(self):
        self.thread_tasks = [t for t in self.thread_tasks if t["task_name"]!= "cps"]

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

            if "prev_inventory" in new_key_types:
                self.mouse.scroll(0, 1)
            elif "next_inventory" in new_key_types:
                self.mouse.scroll(0, -1)

            # we need to run them in a seperate thread as we doin in cps, should we share the same thread for all work??
            if "up_rotate" in new_key_types:
                print("up rotated")
            elif "down_rotate" in new_key_types:
                print("down rotated")

            if "left_rotate" in new_key_types:
                print("left rotated")
            elif "right_rotate" in new_key_types:
                print("right rotated")

        self.prev_mouse_btn_types = current_mouse_btn_types

    def take_action(self, current_keys, current_mouse_btn_types, is_off_hand_palm_open):
        self.current_keys = current_keys
        self.is_off_hand_palm_open = is_off_hand_palm_open
        self.current_mouse_btn_types = current_mouse_btn_types

        self._keyboard()
        self._mouse()
