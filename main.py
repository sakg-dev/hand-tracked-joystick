import cv2
import mediapipe as mp
from tools import draw_hand_landmarks
from core.camera import Camera
from core.gesture_recognizer import Gesture_recognizer
from core.fps import Fps
from config.constants import WIN_NAME, WINDOW_HEIGHT, WINDOW_WIDTH
from core.gesture_mapper import Gesture_mapper
from core.actions_taker import Action_taker


class Joystick:
    def __init__(self):
        self.camera = Camera(0)
        self.gesture_recognizer = Gesture_recognizer()
        self.gesture_mapper = Gesture_mapper()
        self.action_taker = Action_taker()
        self.fps = Fps()

    def prep_img(self, bgr_img):
        """Takes bgr image and return flipped and mediapipe ready rgb img"""
        flipped_frame = cv2.flip(bgr_img, 1)
        img_with_fps = self.fps.set_fps_to_img(flipped_frame, (20, 40), (255, 100, 255))
        rgb_frame = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=cv2.cvtColor(img_with_fps, cv2.COLOR_BGR2RGB)
        )
        return rgb_frame

    def detect_and_process_gesture(self, rgb_frame):
        gestures, handedness, hlm, hwlm = self.gesture_recognizer.recognize(rgb_frame)

        gesture_mapped = self.gesture_mapper.map(
            hlm,
            handedness,
            gestures,
            self.action_taker
        )
        rest_pose_ldms = []
        if gesture_mapped:
            current_keys, current_mouse_btn_types, is_off_hand_palm_open, rest_pose_ldms = gesture_mapped
            self.action_taker.take_action(current_keys, current_mouse_btn_types, is_off_hand_palm_open)

        return [rest_pose_ldms, hlm]
    
    def process_final_img_and_show(self,rgb_frame,hlm,rest_pose_ldms):
        result_img = draw_hand_landmarks(
            rgb_frame.numpy_view(),
            hlm,
            rest_pose_ldms
        )

        resized_result_img = cv2.resize(result_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE | cv2.WINDOW_GUI_NORMAL)
        cv2.imshow(WIN_NAME, resized_result_img)

    def main(self):
        while True:
            try:
                frame = self.camera.read()
                rgb_frame = self.prep_img(frame)
                rest_pose_ldms, hlm = self.detect_and_process_gesture(rgb_frame)
                self.process_final_img_and_show(rgb_frame, hlm, rest_pose_ldms)
                cv2.waitKey(1)
            except:
                print("Quitting")
                break
        self.camera.release()
        cv2.destroyAllWindows()

joystick = Joystick()
joystick.main()