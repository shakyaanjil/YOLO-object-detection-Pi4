from flask import Flask, render_template
from MotorModule import Motor
from YOLOModule import ObjectDetector, Camera
from RedLineModule import RedLineDetector
import cv2

app = Flask(__name__)

motor = Motor(2, 3, 4, 17, 22, 27)

# Initialize YOLOv4 object detector
yolo_weights = "yolov4-tiny-obj_best.weights"
yolo_config = "yolov4-tiny-custom.cfg"
yolo_labels = "obj.names"
target_labels = ['Human', 'Forklift', 'Cone', 'Pallet']  # Adjust this list based on your specific targets
object_detector = ObjectDetector(yolo_weights, yolo_config, yolo_labels, target_labels)

# Initialize red line detector
focal_length = 579.217877094  # Adjust this value based on your camera setup
red_line_height = 0.175  # Adjust this value based on the height of your red line in the frame
red_line_detector = RedLineDetector(focal_length, red_line_height)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move/<direction>')
def mov(direction):
    if direction == 'up':
        motor.move(0.4, 0, 0.1)
    elif direction == 'down':
        motor.move(-0.4, 0, 0.1)
    elif direction == 'left':
        motor.move(0.3, 0.5, 0.1)
    elif direction == 'right':
        motor.move(0.3, -0.5, 0.1)
    return 'Moved ' + direction

@app.route('/stop')
def stop():
    motor.stop(0.1)
    return 'Stopped'

def detect_objects_and_redline(frame):
    # Object detection
    bbox, labels, confidences = object_detector.detect_objects(frame)
    object_detected = any(label in target_labels for label in labels)

    # Red line detection
    frame, red_line_detected = red_line_detector.detect_red_line(frame)

    return object_detected, red_line_detected

def override_control_if_necessary(object_detected, red_line_detected):
    if object_detected:
        print("Objects detected, stopping the vehicle.")
        motor.stop(0.1)
    elif red_line_detected:
        print("Red line detected, stopping the vehicle.")
        motor.stop(0.1)