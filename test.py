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