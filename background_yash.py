import cv2
import numpy as np
import easyocr
from OCR_on_detected import start_OCR
from google_sheet_update import update_sheet
reader = easyocr.Reader(['en'], gpu=True)


def ocr(moment_frame_gray_thresh):
    ladle_number = start_OCR(moment_frame_gray_thresh)
    print(ladle_number)
    # detections = reader.readtext(moment_frame_gray_thresh)
    # cam = 1
    # for detection in detections:
    #     bbox, text, score = detection
    #     if score > 0.5:
    #         print (bbox, text, score)
    #         update_sheet(text,cam)

    # count = 1
    # start_OCR(count,moment_frame_gray_thresh)
    # pass   
    

            



def moment_separation(video_source):
# cap = cv2.VideoCapture('vtest.avi')
    cap = cv2.VideoCapture(video_source)
    
    # out = cv2.VideoWriter("output.avi", fourcc, 5.0, (640,320))

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    print(frame1.shape)
    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            if cv2.contourArea(contour) < 1800:
                continue
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)
            try:
                moment_frame_crop = frame1[int(y):int(h), int(x): int(w), :]
                moment_frame_gray = cv2.cvtColor(moment_frame_crop, cv2.COLOR_BGR2GRAY)
                _,moment_frame_gray_thresh = cv2.threshold(moment_frame_gray, 64, 255, cv2.THRESH_BINARY_INV) 
            #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
                ocr(moment_frame_gray_thresh)
            except:
                pass
            # return (x, y, w, h)
        image = cv2.resize(frame1, (1280,720))
        # out.write(image)
        cv2.imshow("feed", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(1) == 27:
            break
        # return frame1

    cv2.destroyAllWindows()
    cap.release()
    # out.release()

