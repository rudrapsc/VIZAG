import cv2
import numpy as np
img = cv2.imread(r"dataset\images\train\-_mp4-0_jpg.rf.1a75eedd0cf2dfe22c8049bfd401abb9.jpg",cv2.IMREAD_GRAYSCALE)
cap = cv2.VideoCapture(0)

#features
sift = cv2.SIFT_create()
kp_image,desc_image = sift.detectAndCompute(img,None)
img = cv2.drawKeypoints(img,kp_image,img)

#feature mapping
index_params = dict(algorithm=0, trees=5)
search_params= dict()
flann = cv2.FlannBasedMatcher(index_params,search_params)

while True:
    _,frame = cap.read()
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    kp_gray,desc_grayframe= sift.detectAndCompute(gray_frame,None)
    gray_frame= cv2.drawKeypoints(gray_frame,kp_gray,gray_frame)
    matches = flann.knnMatch(desc_image,desc_grayframe,k=2)
    good_points = []
    for m,n in matches:
        if m.distance<0.5*n.distance:
            good_points.append(m)
    img3 = cv2.drawMatches(img,kp_image,gray_frame,kp_gray,good_points,gray_frame)

    # homography

    if len(good_points)>10:
        query_pts = np.float32([kp_image[m.queryIdx].pt])

    cv2.imshow("camera frame gray",gray_frame)
    cv2.imshow("image",img)
    cv2.imshow("image3",img3)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()