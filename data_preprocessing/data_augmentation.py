import cv2
import os
import albumentations as A

# Paths
base_folder = 'C:/Users/Anjil/Documents/ClassOFour'
output_folder_flip = os.path.join(base_folder, 'flipped')
output_folder_rotate = os.path.join(base_folder, 'rotated')

# Make sure output folders exist
os.makedirs(output_folder_flip, exist_ok=True)
os.makedirs(output_folder_rotate, exist_ok=True)

# Define the augmentation pipeline
transform_flip = A.Compose([
    A.HorizontalFlip(p=1.0),
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

transform_rotate = A.Compose([
    A.Rotate(limit=12, p=1.0),
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

# Function to load and transform an image and its annotation
def process_image(image_path, annotation_path, transform, output_folder, suffix):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Load annotation
    with open(annotation_path, 'r') as file:
        bboxes = []
        for line in file:
            parts = line.strip().split()
            if len(parts) == 5:  # Ensure we have class plus four coordinates
                class_id, x_center, y_center, width, height = parts
                # Convert each to float and ensure all coordinates are within the correct range
                x_center, y_center, width, height = map(float, [x_center, y_center, width, height])
                if 0 < x_center <= 1 and 0 < y_center <= 1 and 0 < width <= 1 and 0 < height <= 1:
                    bboxes.append([x_center, y_center, width, height, float(class_id)])
                else:
                    print(f"Invalid bbox in file {annotation_path}: {line}")
                    continue
            else:
                print(f"Skipping malformed line in {annotation_path}: {line}")
                continue

    if not bboxes:
        print(f"No valid bounding boxes found in {annotation_path}. Skipping.")
        return

    # Apply augmentation
    transformed = transform(image=image, bboxes=[bbox[:-1] for bbox in bboxes], class_labels=[int(bbox[-1]) for bbox in bboxes])
    transformed_image = cv2.cvtColor(transformed['image'], cv2.COLOR_RGB2BGR)
    transformed_bboxes = transformed['bboxes']

    # Construct new filenames with suffix
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    new_image_path = os.path.join(output_folder, f"{base_filename}_{suffix}.jpg")
    new_annotation_path = os.path.join(output_folder, f"{base_filename}_{suffix}.txt")

    # Save the transformed image
    cv2.imwrite(new_image_path, transformed_image)

    # Save the transformed annotation
    with open(new_annotation_path, 'w') as file:
        for bbox, label in zip(transformed_bboxes, [bbox[-1] for bbox in bboxes]):
            file.write(f"{int(label)} {' '.join(map(str, bbox))}\n")

# Process each image and its corresponding annotation
for filename in os.listdir(base_folder):
    if filename.endswith('.jpg'):
        image_path = os.path.join(base_folder, filename)
        annotation_path = os.path.join(base_folder, filename.replace('.jpg', '.txt'))
        
        # Check if the annotation file exists
        if os.path.exists(annotation_path):
            # Flip the image and save with '_flip' suffix
            process_image(image_path, annotation_path, transform_flip,
                          output_folder_flip, "flip")
            
            # Rotate the image and save with '_rotate' suffix
            process_image(image_path, annotation_path, transform_rotate,
                          output_folder_rotate, "rotate")
        else:
            print(f"No annotation for {filename}")

print("Augmentation completed.")