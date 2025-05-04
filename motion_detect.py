# motion_detect.py

import cv2 #type: ignore[import]
import numpy as np#type: ignore[import]
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30) 

if not cap.isOpened():
    print("Error: Unable to access camera")
    exit()

ret, frame1 = cap.read()
ret, frame2 = cap.read()

prev_time = time.time()
fps = 0

while cap.isOpened():
    current_time = time.time()
    elapsed = current_time - prev_time
    if elapsed > 0:
        fps = 1.0 / elapsed
    prev_time = current_time
    
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    _, thresh = cv2.threshold(blur, 15, 255, cv2.THRESH_BINARY)
    
    dilated = cv2.dilate(thresh, None, iterations=4)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a copy of the frame for display
    frame_display = frame1.copy()
    
    # Reduce detection threshold for increased sensitivity
    motion_detected = False
    for c in contours:
        if cv2.contourArea(c) < 300:  
            continue
        motion_detected = True
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame_display, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Display information on the image
    cv2.putText(frame_display, f"FPS: {int(fps)}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    if motion_detected:
        cv2.putText(frame_display, "Motion detected!", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Also display the processed frame to see how detection works
    small_thresh = cv2.resize(dilated, (320, 240))
    frame_display[0:240, 0:320] = cv2.cvtColor(small_thresh, cv2.COLOR_GRAY2BGR)
    
    cv2.imshow("Motion Detection", frame_display)
    
    frame1 = frame2
    ret, frame2 = cap.read()
    
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
