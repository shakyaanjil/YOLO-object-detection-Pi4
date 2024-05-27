from flask import Flask, render_template
from MotorModule import Motor
from YOLOModule import ObjectDetector, Camera
from RedLineModule import RedLineDetector
import cv2

app = Flask(__name__)

motor = Motor(2, 3, 4, 17, 22, 27)

@app.route('/')
def index():
    return render_template('index.html')