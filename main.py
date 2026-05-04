import cv2
import time
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
from tools import draw_hand_landmarks
# import uinput
# oir use pynput

cam = cv2.VideoCapture(0)

base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")
option = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2
)
detector = vision.HandLandmarker.create_from_options(option)
pTime = 0
while True:
    success, frame = cam.read()

    cTime = time.time()
    fps = round(1/(cTime-pTime))
    pTime = cTime
    img_with_fps = cv2.putText(frame,str(fps),(20,40),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 100, 255), 2)

    # cv2.imshow("img", frame)
    rgb_img = cv2.cvtColor(img_with_fps, cv2.COLOR_BGR2RGB)
    rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)

    result = detector.detect(rgb_frame)

    result_rgb_img = draw_hand_landmarks(rgb_frame.numpy_view(), result)

    final_bgr_img = cv2.cvtColor(result_rgb_img,cv2.COLOR_RGB2BGR)

    cv2.imshow("img", final_bgr_img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()
