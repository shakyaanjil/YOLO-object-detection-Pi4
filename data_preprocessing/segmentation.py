import os
import cv2
import shutil

image_folder = 'C:/Users/Anjil/Documents/UnAnnotated1'
annotation_folder = 'C:/Users/Anjil/Documents/UnAnnotated1'
output_base_folder = 'C:/Users/Anjil/Documents/pi_phase1/segmented_images' #directory to save segmented images

no_annotation_folder = 'C:/Users/Anjil/Documents/UnAnnotated2' #directory to save images with no annotations


def segmentation():
    class_names = ['Human', 'Pallet', 'Cone', 'Box']  
    for class_name in class_names:
        os.makedirs(os.path.join(output_base_folder, class_name), exist_ok=True)

    for filename in os.listdir(annotation_folder):
        if filename.endswith('.txt'):
            image_path = os.path.join(image_folder, filename.replace('.txt', '.jpg'))
            annotation_path = os.path.join(annotation_folder, filename)
            image = cv2.imread(image_path)
            height, width, _ = image.shape
            with open(annotation_path, 'r') as file:
                for line in file:
                    class_id, x_center, y_center, bbox_width, bbox_height = map(float, line.split())
                    x_center, y_center = x_center * width, y_center * height
                    bbox_width, bbox_height = bbox_width * width, bbox_height * height
                    x_min = int(x_center - bbox_width / 2)
                    y_min = int(y_center - bbox_height / 2)
                    x_max = int(x_center + bbox_width / 2)
                    y_max = int(y_center + bbox_height / 2)
                    # Crop image
                    cropped_image = image[y_min:y_max, x_min:x_max]
                    output_folder = os.path.join(output_base_folder, class_names[int(class_id)])
                    cv2.imwrite(os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_{class_id}.jpg'), cropped_image)
            
def filter_image():
    os.makedirs(no_annotation_folder, exist_ok=True)
    image_files = set([f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')])
    annotation_files = set([f.replace('.txt', '.jpg') for f in os.listdir(annotation_folder) if f.endswith('.txt')])
    images_without_annotations = image_files - annotation_files
    for image in images_without_annotations:
        original_path = os.path.join(image_folder, image)
        new_path = os.path.join(no_annotation_folder, image)
        shutil.move(original_path, new_path)  

segmentation()
filter_image()

