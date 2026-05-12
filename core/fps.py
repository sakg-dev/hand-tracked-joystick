import time
import cv2


class Fps:
    def __init__(self):
        self.prev_time = 0

    def set_fps_to_img(self, img, coords, color):
        current_time = time.time()
        fps = round(1/(current_time - self.prev_time))

        img_with_fps = cv2.putText(img, str(fps), coords, cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        self.prev_time = current_time

        return img_with_fps