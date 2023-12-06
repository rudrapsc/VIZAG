import cv2 as cv
import numpy as np
import os
from google.cloud import vision

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def detect_text_with_positions(client, content):
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    annotations = response.text_annotations
    return annotations

def process_grid(image, client, grid):
    h_start, h_end, w_start, w_end = grid
    grid_img = image[h_start:h_end, w_start:w_end]
    content = cv.imencode('.jpg', grid_img)[1].tobytes()
    texts = detect_text_with_positions(client, content)

    detected_texts = []
    for text in texts[1:]:
        text_content = text.description.replace('\n', ' ')
        if text_content.isnumeric():  # Check if the text is numeric
            vertices = [(vertex.x + w_start, vertex.y + h_start) for vertex in text.bounding_poly.vertices]
            cv.polylines(image, [np.array(vertices, np.int32)], True, (0, 255, 0), 3)
            detected_texts.append(text_content)

    return image, detected_texts

def draw_grid_lines(image, grid_size):
    h, w = image.shape[:2]
    slice_height, slice_width = h // grid_size, w // grid_size

    for i in range(1, grid_size):
        cv.line(image, (0, i * slice_height), (w, i * slice_height), (255, 255, 255), 1)
        cv.line(image, (i * slice_width, 0), (i * slice_width, h), (255, 255, 255), 1)

def process_image_in_grids(image, client, grid_size):
    all_texts = []
    for i in range(grid_size):
        for j in range(grid_size):
            grid = (i * image.shape[0] // grid_size, (i + 1) * image.shape[0] // grid_size, 
                    j * image.shape[1] // grid_size, (j + 1) * image.shape[1] // grid_size)
            image, detected_texts = process_grid(image, client, grid)
            all_texts.extend(detected_texts)
    draw_grid_lines(image, grid_size)
    return image, all_texts

def process_directory(count, image, client):
    findings_dir = "Findings"
    create_directory(findings_dir)
    
    processed_image, detected_texts = process_image_in_grids(np.copy(image), client, 1)  # Assuming grid_size is always 1
    if detected_texts:
        detected_text_str = '_'.join(detected_texts).replace(' ', '_')
        output_path = os.path.join(findings_dir, f'{detected_text_str}.jpg')
    else:
        output_path = os.path.join(findings_dir, f'no_numbers_detected_{count}.jpg')
    cv.imwrite(output_path, processed_image)

def start_OCR(count, img):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "collablens-bucket_key.json"  # Update the path
    client = vision.ImageAnnotatorClient()
    process_directory(count, img, client) 

if __name__ == '__main__':
    # Example usage
    img = cv.imread("path_to_your_image.jpg")  # Update with your image path
    start_OCR(1, img)  # Example count
