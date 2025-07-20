import cv2 
import numpy as np
import easyocr

image= cv2.imread("OCR/photos/n.png")

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

white_mask = cv2.inRange(gray,200,255)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
closed_mask = cv2.morphologyEx(white_mask, cv2.MORPH_CLOSE, kernel)

contours, _ = cv2.findContours(closed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
filled_mask = np.zeros_like(closed_mask)
cv2.drawContours(filled_mask, contours, -1, 255, thickness=cv2.FILLED)

small = cv2.resize(filled_mask, (14, 14), interpolation=cv2.INTER_AREA)
smoothed_mask = cv2.resize(small, (256, 256), interpolation=cv2.INTER_CUBIC)
cv2.imshow("Smoothed Mask", smoothed_mask)


reader = easyocr.Reader(['en'])

result = reader.readtext(smoothed_mask)

for detection in result:
    bbox, text, confidence = detection
    print(f"Detected Text: {text} (Confidence: {confidence:.2f})")

cv2.imwrite('connected_mask.png', filled_mask)
cv2.imshow('Connected Mask', filled_mask)
cv2.imshow("Original",image)
cv2.imshow("White Mask",white_mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
