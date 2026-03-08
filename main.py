
"""
# 1. IMPORT
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 2. LOAD DATA
df = pd.read_csv("data/your_file.csv")
print(df.head())

# 3. EXPLORE
print(df.shape)
print(df.describe())
df.hist()
plt.show()

# 4. PREPARE
X = df.drop("target", axis=1)   # features
y = df["target"]                 # label

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. TRAIN
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 6. EVALUATE
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))

# 7. SAVE MODEL
import pickle
pickle.dump(model, open("models/model.pkl", "wb"))
"""

import cv2
from ultralytics import YOLO

# Load pretrained YOLO model
model = YOLO("yolov8n.pt")

# ESP32 stream URL
stream_url = "http://192.168.1.45:81/"

cap = cv2.VideoCapture(stream_url)

while True:

    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    results = model(frame)

    people_count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])

            # COCO class 0 = person
            if cls == 0:
                people_count += 1

                x1,y1,x2,y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

    cv2.putText(frame,f"People: {people_count}",
                (20,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                2)

    cv2.imshow("Bus Camera AI",frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()