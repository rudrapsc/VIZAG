import cv2
import os
import threading
from OCR_on_detected import start_OCR

def save_cropped_images(frame, contours, output_dir, count):
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 900:  # Adjust this threshold as needed
            continue
        cropped_image = frame[y:y+h, x:x+w]
        thread = threading.Thread(target=start_OCR, args=(count, cropped_image))
        thread.start()
        count += 1
    return count

cap = cv2.VideoCapture(0)  # Change this to your video path

cropped_img_dir = "cropped_images"
os.makedirs(cropped_img_dir, exist_ok=True)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

count = 0
while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    count = save_cropped_images(frame1, contours, cropped_img_dir, count)

    frame1 = frame2
    ret, frame2 = cap.read()
    cv2.imshow("Frame", frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
