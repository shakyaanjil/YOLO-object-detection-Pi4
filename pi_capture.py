import os
import cv2
import time
from cvlib.object_detection import YOLO

weights = "C:/Users/Anjil/Documents/pi_phase1/4ClassWeights/yolov4-tiny-obj_best.weights"
config = "C:/Users/Anjil/Documents/pi_phase1/yolov4-tiny-custom.cfg"
labels_path = "C:/Users/Anjil/Documents/pi_phase1/obj.names"

yolo = YOLO(weights, config, labels_path)
save_dir = "C:/Users/Anjil/Documents/pi_phase1/detected_images"
os.makedirs(save_dir, exist_ok=True)  

target_labels = ['Human', 'Pallet', 'Cone', 'Box'] # add classes 

real_widths = {
    'Human': 0.3,  # width in meters
    'Pallet': 0.5,
    'Cone': 0.05,
    'Box': 0.4,
}

def handle_detections(frame, bbox, labels, confidences, target_labels):
    detected_objects = {}
    for label, confidence in zip(labels, confidences):
        if label in target_labels:
            if label not in detected_objects:
                detected_objects[label] = []
            detected_objects[label].append(confidence)
    
    if detected_objects:
        print("Detected target objects:", detected_objects)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(save_dir, f'detection_{timestamp}.jpg')
        cv2.imwrite(filename, frame)
        #print(f"Saved detected image to {filename}")
        return True, detected_objects
    return False, None

def calculate_distance_by_width(focal_length, real_width, perceived_width):
    if perceived_width == 0:
        return float('inf') 
    return (focal_length * real_width) / perceived_width
focal_length = 579.217877094  # focal length in pixels (depends on the camera)

cap = cv2.VideoCapture(0)  
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 416)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 416)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    bbox, labels, confs = yolo.detect_objects(frame)
    for box, label, conf in zip(bbox, labels, confs):
        x, y, w, h = box
        yolo.draw_bbox(frame, [box], [label], [conf])
        detected, detected_objects = handle_detections(frame, bbox, labels, confs, target_labels)

    cv2.imshow('frame:', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
