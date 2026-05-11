from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class Gesture_recognizer:
    def __init__(self, model_path="./models/gesture_recognizer.task", num_hands=2):
        base_option = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(
            base_options=base_option,
            num_hands=num_hands
        )
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def recognize(self, rgb_frame):
        r = self.recognizer.recognize(rgb_frame)
        return [r.gestures, r.handedness, r.hand_landmarks, r.hand_world_landmarks]

    def close(self):
        self.recognizer.close()