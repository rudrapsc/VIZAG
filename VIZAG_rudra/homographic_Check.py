import cv2 as cv
import os
import numpy as np

class getCode:
    def __init__(self, references_folder):
        self.descriptors = {}
        self.ref_image_files = []

        all_references = os.listdir(references_folder)
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        self.ref_image_files = [f for f in all_references if any(f.lower().endswith(ext) for ext in image_extensions)]

        self.build_descriptors(references_folder)

    def build_descriptors(self, references_folder):
        sift = cv.SIFT_create()
        for image_file in self.ref_image_files:
            ref_image_path = os.path.join(references_folder, image_file)
            img = cv.imread(ref_image_path, cv.IMREAD_GRAYSCALE)
            assert img is not None, "Could not read the image."
            _, descriptors = sift.detectAndCompute(img, None)
            self.descriptors[image_file] = descriptors

    def match_with_webcam(self, frame):
        sift = cv.SIFT_create()
        bf = cv.BFMatcher(cv.NORM_L2, crossCheck=True)

        try:
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            _, descriptors_frame = sift.detectAndCompute(gray_frame, None)

            best_match = "no match"
            max_matches = 0

            for ref_image_name, descriptors_ref in self.descriptors.items():
                matches = bf.match(descriptors_ref, descriptors_frame)
                num_good_matches = len(matches)

                if num_good_matches > max_matches:
                    max_matches = num_good_matches
                    best_match = ref_image_name

            return max_matches
        except Exception as e:
            print(f"exception is: {e}")
            return 0

# Usage example
if __name__ == "__main__":
    references_folder = r"C:\VIZAG\ref"  # Replace with your folder path
    matcher = getCode(references_folder)
    # Example of using match_with_webcam with a loaded image
    # test_image = cv.imread('path_to_test_image.jpg')
    # matcher.match_with_webcam(test_image)
