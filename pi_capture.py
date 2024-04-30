import cv2
from cvlib.object_detection import YOLO

weights = "C:/Users/Anjil/Documents/pi_phase1/4ClassWeights/yolov4-tiny-obj_best.weights"
config = "C:/Users/Anjil/Documents/pi_phase1/yolov4-tiny-custom.cfg"
labels_path = "C:/Users/Anjil/Documents/pi_phase1/obj.names"

yolo = YOLO(weights, config, labels_path)

cap = cv2.VideoCapture(0)  

while True:
    ret, frame = cap.read()
    if not ret:
        break
    bbox, labels, confs = yolo.detect_objects(frame)
    for box, label, conf in zip(bbox, labels, confs):
        x, y, w, h = box
        yolo.draw_bbox(frame, [box], [label], [conf])

    cv2.imshow('frame:', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
