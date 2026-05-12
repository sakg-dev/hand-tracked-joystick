import cv2
import mediapipe as mp

cam = cv2.VideoCapture(0)

while True:
    success, frame = cam.read()

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()