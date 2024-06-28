import cv2
import csv
import numpy as np
from scipy.spatial import distance as dist
from collections import OrderedDict

color_rgb = np.uint8([[[255, 116, 23]]])

# Convert the RGB color to HSV
color_hsv = cv2.cvtColor(color_rgb, cv2.COLOR_RGB2HSV)
hsv_value = color_hsv[0][0]
print("HSV value:", hsv_value)

# Extract H, S, V values
h, s, v = hsv_value

# Define the range with some tolerance
tolerance = 10
color_lower = np.array([max(h - tolerance, 0), 100, 100])
color_upper = np.array([min(h + tolerance, 179), 255, 255])

print("HSV lower bound:", color_lower)
print("HSV upper bound:", color_upper)

# Define a simple object tracker using centroids
class CentroidTracker:
    def __init__(self, maxDisappeared=50, maxTrackers=10):
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.maxDisappeared = maxDisappeared
        self.maxTrackers = maxTrackers
    
    def register(self, centroid):
        if len(self.objects) < self.maxTrackers:
            self.objects[self.nextObjectID] = centroid
            self.disappeared[self.nextObjectID] = 0
            self.nextObjectID += 1
    
    def deregister(self, objectID):
        del self.objects[objectID]
        del self.disappeared[objectID]
    
    def update(self, inputCentroids):
        if len(inputCentroids) == 0:
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
            return self.objects
        
        if len(self.objects) == 0:
            for i in range(len(inputCentroids)):
                self.register(inputCentroids[i])
        else:
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())
            D = dist.cdist(np.array(objectCentroids), inputCentroids)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            usedRows = set()
            usedCols = set()
            
            for (row, col) in zip(rows, cols):
                if row in usedRows or col in usedCols:
                    continue
                objectID = objectIDs[row]
                self.objects[objectID] = inputCentroids[col]
                self.disappeared[objectID] = 0
                usedRows.add(row)
                usedCols.add(col)
            
            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)
            
            if D.shape[0] >= D.shape[1]:
                for row in unusedRows:
                    objectID = objectIDs[row]
                    self.disappeared[objectID] += 1
                    if self.disappeared[objectID] > self.maxDisappeared:
                        self.deregister(objectID)
            else:
                for col in unusedCols:
                    self.register(inputCentroids[col])
        
        return self.objects

# Initialize our centroid tracker with a maximum number of trackers
maxTrackers = 1
ct = CentroidTracker(maxTrackers=maxTrackers)

# Function to find and print the centroid of the detected color blob
def find_color_centroid(frame, time):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_lower, color_upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    inputCentroids = []
    with open("capturedy.csv", "a") as y, open("capturedx.csv", "a") as x:
        writery = csv.writer(y)
        writerx = csv.writer(x)
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    inputCentroids.append((cx, cy))
        
        objects = ct.update(inputCentroids)
        
        for (objectID, centroid) in objects.items():
            text = "ID {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
            print(f"object{text} (x,y): ({centroid[0]},{centroid[1]})")
            writery.writerow([time, centroid[1]])
            writerx.writerow([time, centroid[0]])
        return frame

# Main function to capture video from webcam and detect the color
def detect_color_objects(camera):
    with open("capturedy.csv", "w") as f, open("capturedx.csv", "w") as g:
        f.truncate()
        g.truncate()
    cap = cv2.VideoCapture(camera)
    time = 0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to capture frame from webcam. Exiting...")
            break
        
        frame = cv2.flip(frame, 1)
        frame_with_centroid = find_color_centroid(frame, time)
        time += 1
        cv2.imshow('Color Detection', frame_with_centroid)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Run the color detection function
