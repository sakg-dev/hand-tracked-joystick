import os
import sys
path = os.path.abspath(".")
sys.path.insert(0, path)
from tools import randomize_int
from config.constants import LEFT_CPS, RIGHT_CPS, CPS_MAX_RAND_FACTOR
from pynput.keyboard import Controller as kController
from pynput.mouse import Button, Controller as mController
from time import sleep, time
import threading


class Action_taker:
    def __init__(self):
        self.keyboard = kController()
        self.mouse = mController()

        self.prev_keys = []
        self.prev_mouse_btn_types = []
        
        self.is_thread_running = True
        self.thread_tasks = []
        self.thread = threading.Thread(target=self._thread_work)
        self.rotate_speed = 1
        self.thread_lowest_task_sleep_interval = 0.001
        self.thread.start()

    def _thread_work(self):
        # sleep interval is not random everytime, make a function to radomise value based on given values and change it on every time you do last_ran assign
        while self.is_thread_running:
            current = time()
            if len(self.thread_tasks) > 0:
                self.thread_lowest_task_sleep_interval = min(list(map(lambda t: t["sleep_interval"], self.thread_tasks)))
                for t in self.thread_tasks:
                    task_name, func, args, sleep_interval, last_ran = t["task_name"], t["func"], t["args"], t["sleep_interval"], t["last_ran"]
                    if current - last_ran >= sleep_interval:
                        # print(sleep_interval)
                        func(*args)
                        t["last_ran"] = current
            else:
                self.thread_lowest_task_sleep_interval = 0.001 # in case it has been modifed..
            sleep(self.thread_lowest_task_sleep_interval)
                    

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

    def _cps_loop(self, btn):
        self.mouse.click(btn)

    def _hold_press(self, btn):
        self.mouse.press(btn)

    def _hold_release(self, btn):
        self.mouse.release(btn)

    def _cps_start(self, btn):
        cps = LEFT_CPS if self.is_off_hand_palm_open == False else RIGHT_CPS
        self.thread_tasks.append({
            "task_name": "cps",
            "func": self._cps_loop,
            "args": [btn],
            "sleep_interval": randomize_int(int(1000/cps), CPS_MAX_RAND_FACTOR)/1000,
            "last_ran": 0
        })

    def _cps_end(self):
        self.thread_tasks = [t for t in self.thread_tasks if t["task_name"]!= "cps"]
    
    def _stop_thread(self):
        self.is_thread_running = False
        self.thread.join()
    
    def _rotate(self, side):
        val = self.rotate_speed
        x = 0
        y = 0
        if side == "left":
            x = -val
        elif side == "right":
            x = val
        if side == "up":
            y = -val
        elif side == "down":
            y = val
        sleep_interval = 0.01
        self.thread_tasks.append({
            "task_name": f"{side}_rotate",
            "func": lambda x,y: self.mouse.move(x,y),
            "args": [x,y],
            "sleep_interval": sleep_interval,
            "last_ran": 0
        })
    
    def _rotate_remove(self, side):
        self.thread_tasks = [t for t in self.thread_tasks if t["task_name"]!= f"{side}_rotate"]

    def _mouse(self):
        btn = Button.left if self.is_off_hand_palm_open == False else Button.right
        prev_mouse_btn_types = self.prev_mouse_btn_types
        current_mouse_btn_types = self.current_mouse_btn_types

        if len(current_mouse_btn_types) == 0:
            if len(prev_mouse_btn_types) > 0:
                # If current mouse btn is none but prev had
                if "hold" in prev_mouse_btn_types:
                    self._hold_release(btn)
                if "high_cps" in prev_mouse_btn_types:
                    self._cps_end()
                if "up_rotate" in prev_mouse_btn_types:
                    self._rotate_remove("up")
                elif "down_rotate" in prev_mouse_btn_types:
                    self._rotate_remove("down")
                if "left_rotate" in prev_mouse_btn_types:
                    self._rotate_remove("left")
                elif "right_rotate" in prev_mouse_btn_types:
                    self._rotate_remove("right")
        else:
            not_anymore_key_types = list(set(prev_mouse_btn_types) - set(current_mouse_btn_types))
            if len(not_anymore_key_types) != 0:
                # were keys prev time but not anymore
                if "hold" in not_anymore_key_types:
                    self._hold_release(btn)
                if "high_cps" in not_anymore_key_types:
                    self._cps_end()
                if "up_rotate" in prev_mouse_btn_types:
                    self._rotate_remove("up")
                elif "down_rotate" in prev_mouse_btn_types:
                    self._rotate_remove("down")
                if "left_rotate" in prev_mouse_btn_types:
                    self._rotate_remove("left")
                elif "right_rotate" in prev_mouse_btn_types:
                    self._rotate_remove("right")

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
                self._rotate("up")
            elif "down_rotate" in new_key_types:
                self._rotate("down")
            if "left_rotate" in new_key_types:
                self._rotate("left")
            elif "right_rotate" in new_key_types:
                self._rotate("right")

        self.prev_mouse_btn_types = current_mouse_btn_types

    def take_action(self, current_keys, current_mouse_btn_types, is_off_hand_palm_open):
        self.current_keys = current_keys
        self.is_off_hand_palm_open = is_off_hand_palm_open
        self.current_mouse_btn_types = current_mouse_btn_types

        self._keyboard()
        self._mouse()