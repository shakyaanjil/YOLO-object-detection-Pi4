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