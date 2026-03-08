import cv2
import numpy as np
import requests
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

stream_url = "http://192.168.4.1:81/stream"

print("Connecting to stream...")
stream = requests.get(stream_url, stream=True, timeout=10)
print(f"Connected! Status code: {stream.status_code}")

bytes_data = bytes()

for chunk in stream.iter_content(chunk_size=65536):
    bytes_data += chunk

    a = bytes_data.find(b'\xff\xd8')
    b = bytes_data.find(b'\xff\xd9')

    if a != -1 and b != -1:
        jpg = bytes_data[a:b+2]
        bytes_data = bytes_data[b+2:]

        # Skip if JPEG is too small to be a real frame
        if len(jpg) < 1000:
            continue

        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        if frame is None:
            continue

        print(f"Got frame! Size: {frame.shape}")

        results = model(frame)
        people_count = 0

        for r in results:
            for box in r.boxes:
                if int(box.cls[0]) == 0:
                    people_count += 1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.putText(frame, f"People: {people_count}",
                    (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2)

        cv2.imshow("Bus Camera AI", frame)

        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()