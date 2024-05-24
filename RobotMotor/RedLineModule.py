import cv2
import numpy as np

class Camera:
    def __init__(self, video_path):
        self.video_capture = cv2.VideoCapture(video_path)

    def get_frame(self):
        ret, frame = self.video_capture.read()
        return frame if ret else None

    def release(self):
        self.video_capture.release()

class RedLineDetector:
    def __init__(self, focal_length, red_line_height):
        self.focal_length = focal_length
        self.red_line_height = red_line_height

    def detect_red_line(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_bound = np.array([160, 50, 50])
        upper_bound = np.array([180, 255, 255])

        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w >= 700:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                distance = (self.focal_length * self.red_line_height) / h
                print(f"Distance to red line: {distance} meters")

                if distance < 1.0:
                    return frame, True

        return frame, False
    
# Define the focal length and height of the red line
focal_length = 579
red_line_height = 0.175

# Create an instance of the Camera class
camera = Camera(0)

# Create an instance of the RedLineDetector class
detector = RedLineDetector(focal_length, red_line_height)

while True:
    frame = camera.get_frame()
    if frame is None:
        break

    frame_with_red_line, red_line_detected = detector.detect_red_line(frame)

    cv2.imshow('Video', frame_with_red_line)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

    if red_line_detected:
        print("停止 Stop command assigned")

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()