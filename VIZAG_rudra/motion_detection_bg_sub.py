import cv2
import os
import threading
from OCR_on_detected import start_OCR
import concurrent.futures
from homographic_Check import getCode
global matcher
# matcher = getCode()
import cv2
import os
import concurrent.futures
from homographic_Check import getCode  # Make sure this import is correct

# Initialize the matcher object
references_folder = r"ref"  # Replace with your folder path
matcher = getCode(references_folder)

def save_cropped_images(frame, contours, output_dir, count=0):
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 900:
                continue
            cropped_image = frame[y:y+h, x:x+w]
            n_matches = matcher.match_with_webcam(cropped_image) #this
            
            if n_matches > 80: #thi
                print(f'matches is: {n_matches}')
                future = executor.submit(start_OCR, cropped_image)  # Make sure start_OCR function is defined
                futures.append(future)

                results = [future.result() for future in futures]
                return results
    return None

cap = cv2.VideoCapture(r"C:\VIZAG\stable.mp4")
cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    results = save_cropped_images(frame1, contours, "cropped_images")
    print("number is:", results)

    frame1 = frame2
    ret, frame2 = cap.read()

    cv2.imshow("Frame", frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
