import numpy as np
import cv2
import csv

cap = cv2.VideoCapture(1)
with open("captured.csv", "w") as captured:
    captured.truncate
    writer = csv.writer(captured)
    while(True):
        ret, captured_frame = cap.read()
        output_frame = captured_frame.copy()
        captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR)
        captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
        captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)
        # Possible yellow threshold: [20, 110, 170][255, 140, 215]
        # Possible blue threshold: [20, 115, 70][255, 145, 120]
        ranges = [[20, 150, 150],[190, 255, 255]]
        captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array(ranges[0]), np.array(ranges[1]))
        captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
        circles = cv2.HoughCircles(captured_frame_lab_red, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_red.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=60)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for circle in circles:
                if (circle[2]**2)*3 >= 100:
                    cv2.circle(output_frame, center=(circle[0], circle[1]), radius=circle[2], color=(0, 255, 0), thickness=2)
                    print([circles[0,0], circles[0, 1]])
        cv2.imshow('frame', output_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()