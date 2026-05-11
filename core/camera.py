import cv2

class Camera:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")

    def read(self):
        success, frame = self.cap.read()

        if not success:
            raise RuntimeError("Could not read camera")

        return frame

    def release(self):
        self.cap.release()
