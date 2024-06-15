import cv2
import csv
import math







def capture(directory):
    vid = cv2.VideoCapture(directory)
    detector = cv2.createBackgroundSubtractorMOG2()
    counter = 0


    with open("captured.csv", mode="w") as captured:
        captured.truncate()
        write = csv.writer(captured)

        while(vid.isOpened()):

            ret, frame = vid.read() 

            mask = detector.apply(frame)

            _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for n in contours:
                area = cv2.contourArea(n)

                if area > 100:
                    x, y, w, h = cv2.boundingRect(n)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    write.writerow([counter, (h//2)+y])
            counter += 1
            if ret == True:
                cv2.imshow("frame", frame)

            if ret == False:
                break

    vid.release() 
    
    cv2.destroyAllWindows() 
