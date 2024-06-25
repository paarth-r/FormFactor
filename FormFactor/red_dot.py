import numpy as np
import cv2
import csv


def red_dot(vidstream):

    cap = cv2.VideoCapture(vidstream)

    with open("captured.csv", mode="w") as captured:
            captured.truncate()
            write = csv.writer(captured)

    while(True):
        ret, captured_frame = cap.read()
        output_frame = captured_frame.copy()
        captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR)
        captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
        captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)
        lower_red = np.array([160,50,50])
        upper_red = np.array([180,255,255])  
        captured_frame_lab_red = cv2.inRange(captured_frame_lab, lower_red, upper_red)
        captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
        circles = cv2.HoughCircles(captured_frame_lab_red, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_red.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=60)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            cv2.circle(output_frame, center=(circles[0, 0], circles[0, 1]), radius=circles[0, 2], color=(0, 255, 0), thickness=2)
            print(circles[0, 0], circles[0, 1])
        if ret:
            cv2.imshow('frame', output_frame)
        if not ret:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()



def obj_from_colour(vidstream):

    with open("captured.csv", mode="w") as captured:
        captured.truncate()
        write = csv.writer(captured)
        cap = cv2.VideoCapture(vidstream)
        counter = 0
        while(1):

            # Take each frame
            ret, frame = cap.read()

            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
            # define range of red color in HSV
            lower_red = np.array([170, 70, 50])
            upper_red = np.array([180, 255, 255])  
            lower_red2 = np.array([0, 70, 50])
            upper_red2 = np.array([10, 255, 255])  
            #Threshold the HSV image to get only red colors
            mask = cv2.inRange(hsv, lower_red, upper_red)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            # Bitwise-AND mask and original image6
            res = cv2.bitwise_and(frame,frame, mask=mask)
        
            #adding 2 more channels on the mask so we can stack it along other images
            mask_3 = cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR)
            circles = cv2.HoughCircles(mask2, cv2.HOUGH_GRADIENT, 1, mask.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=60)
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                cv2.circle(frame, center=(circles[0, 0], circles[0, 1]), radius=circles[0, 2], color=(0, 255, 0), thickness=2)
                print(circles[0, 0], circles[0, 1])
                write.writerow([counter, circles[0, 1]])
                counter += 1
            # stacking up all three images together
            stacked = np.hstack((mask_3,frame,res))
            if ret:
                cv2.imshow('Result',cv2.resize(stacked,None,fx=0.8,fy=0.8))
            else:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
 
    cv2.destroyAllWindows()
    cap.release()