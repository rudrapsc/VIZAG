import cv2
import os
import threading
from OCR_on_detected import start_OCR
import concurrent.futures
from google_sheet_update import update_sheet
from datetime import datetime,date
def ocr2(frame, contours, output_dir, count=0):
    futures = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 900:
                continue
            cropped_image = frame[y:y+h, x:x+w]
            future = executor.submit(start_OCR, cropped_image)
            futures.append(future)
            # count += 1

    # Collect the results
    results = [future.result() for future in futures]
    print("number is::",results)
    print(type(results))
    cam = 1
    numeric_parts = [int(item) for sublist in results for item in sublist if item.isdigit()]
    try:
        numeric_parts = numeric_parts[0]

        print(numeric_parts)
        print("type of numeric part is",type(numeric_parts))
        time=datetime.now().strftime('%H:%M:%S')
        if numeric_parts == 69 or numeric_parts ==13 or numeric_parts == 23 or numeric_parts == 71 or numeric_parts ==24:
           
            update_sheet(numeric_parts,cam,time)
        
    except:
        pass
# cap = cv2.VideoCapture(0)  # Change this to your video path

cropped_img_dir = "cropped_images"
os.makedirs(cropped_img_dir, exist_ok=True)

def moment_separation(video_source):
    cap = cv2.VideoCapture(video_source)

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

        count = ocr2(frame1, contours, cropped_img_dir, count)

        frame1 = frame2
        ret, frame2 = cap.read()
        cv2.imshow("Frame", frame1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
