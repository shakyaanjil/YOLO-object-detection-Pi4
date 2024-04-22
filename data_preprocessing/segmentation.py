import os
import cv2

image_folder = 'C:/Users/Anjil/Documents/UnAnnotated1'
annotation_folder = 'C:/Users/Anjil/Documents/UnAnnotated1'
output_base_folder = 'C:/Users/Anjil/Documents/pi_phase1/segmented_images' #directory to save segmented images


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

segmentation()

