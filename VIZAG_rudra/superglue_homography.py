import cv2
import os
import subprocess
from pathlib import Path
import tempfile
import shutil
def match_with_webcam(ref_image_path, main_dir='homography'):
    img_dir = os.path.join(main_dir, 'grids')
    output_dir = os.path.join(main_dir, 'matches')
    webcam_dir = os.path.join(main_dir, 'webcam_images')

    # Create directories if they don't exist
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(webcam_dir, exist_ok=True)

    # Copy the reference image to the grids directory
    ref_image_copy_path = os.path.join(img_dir, Path(ref_image_path).name)
    shutil.copy(ref_image_path, ref_image_copy_path)

    cap = cv2.VideoCapture(0)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Save the current webcam frame
        webcam_image_filename = f'webcam_frame_{frame_count}.jpg'
        webcam_image_path = os.path.join(webcam_dir, webcam_image_filename)
        cv2.imwrite(webcam_image_path, frame)

        # Prepare for SuperGlue matching
        with open(os.path.join(img_dir, 'compare.txt'), 'w') as f:
            f.write(f'{Path(ref_image_copy_path).name} {webcam_image_filename}\n')

        # Run SuperGlue
        subprocess.run([
            'python', 'SuperGluePretrainedNetwork/match_pairs.py',
            '--input_pairs', os.path.join(img_dir, 'compare.txt'),
            '--input_dir', img_dir,
            '--output_dir', output_dir,
            '--max_keypoints', '1000',
            '--match_threshold', '0.80',
            '--viz', '--fast_viz', '--force_cpu'
        ], check=True)

        # Display matches (assumes match_pairs.py saves a visualization image)
        match_visualization_path = os.path.join(output_dir, f'{Path(ref_image_copy_path).stem}_{webcam_image_filename}_matches.png')
        if os.path.exists(match_visualization_path):
            match_visualization = cv2.imread(match_visualization_path)
            cv2.imshow('Matches', match_visualization)

        frame_count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Usage
ref_image_path = r"C:\VIZAG\ladle24.jpg"  # Replace with the path to your reference image
match_with_webcam(ref_image_path)
