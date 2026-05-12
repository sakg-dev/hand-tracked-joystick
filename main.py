import cv2
import mediapipe as mp
from tools import draw_hand_landmarks, quit_and_release
from core.camera import Camera
from core.gesture_recognizer import Gesture_recognizer
from core.fps import Fps
from config.constants import WIN_NAME, WINDOW_HEIGHT, WINDOW_WIDTH
from core.gesture_mapper import Gesture_mapper
from core.actions_taker import Action_taker

camera = Camera(0)
gesture_recognizer = Gesture_recognizer()
gesture_mapper = Gesture_mapper()
action_taker = Action_taker()
fps = Fps()


while True:
    try:
        frame = camera.read()
        flipped_frame = cv2.flip(frame, 1)
        img_with_fps = fps.set_fps_to_img(flipped_frame, (20, 40), (255, 100, 255))
        rgb_frame = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=cv2.cvtColor(img_with_fps, cv2.COLOR_BGR2RGB)
        )

        gestures, handedness, hlm, hwlm = gesture_recognizer.recognize(rgb_frame)

        gesture_mapped = gesture_mapper.map(
            hlm,
            handedness,
            gestures
        )
        rest_pose_ldms = []
        if gesture_mapped:
            current_keys, current_mouse_btn_type, is_off_hand_palm_open, rest_pose_ldms = gesture_mapped
            action_taker.take_action(current_keys, current_mouse_btn_type, is_off_hand_palm_open)

        result_img = draw_hand_landmarks(
            rgb_frame.numpy_view(),
            hlm,
            rest_pose_ldms
        )

        resized_result_img = cv2.resize(result_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE | cv2.WINDOW_GUI_NORMAL)
        cv2.imshow(WIN_NAME, resized_result_img)

        if cv2.waitKey(1) & 0xFF == 27:
            quit_and_release(current_keys)
    except:
        print("Quitting")
        break

camera.release()
cv2.destroyAllWindows()
