import cv2
import numpy as np
import os
from ultralytics import YOLO  # Changed import for YOLOv8

# Create a named window first and set any desired flags
cv2.namedWindow("Object Detection", cv2.WINDOW_NORMAL)
# droidcam_url = "http://192.168.0.184:4747/video"
# cap = cv2.VideoCapture(droidcam_url)

# Load custom trained YOLOv8 model
model = YOLO('models/yolov3/ewastebest.pt')  # Changed to YOLOv8 model loading
model.fuse()  # Optimize model for inference

# Load class labels from the model
classes = model.names  # Get class names from the model

DETECTION_FILE = "detections.txt"

def save_detections(objects):
    """Save detected objects to text file"""
    try:
        # Read existing detections
        existing = set()
        if os.path.exists(DETECTION_FILE):
            with open(DETECTION_FILE, "r") as f:
                existing = set(line.strip() for line in f.readlines())
        
        # Add new detections
        new_objects = objects - existing
        if new_objects:
            with open(DETECTION_FILE, "a") as f:  # Append mode
                for obj in new_objects:
                    normalized = obj.lower().replace(" ", "_")
                    f.write(normalized + "\n")
            return True
        return False
    except Exception as e:
        print(f"Error saving detections: {e}")
        return False

# Initialize video capture
cap = cv2.VideoCapture(0)
detected_objects = set()  # Track unique detected objects

# Clear detection file at start
if os.path.exists(DETECTION_FILE):
    os.remove(DETECTION_FILE)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # YOLOv8 inference
        results = model(frame, verbose=False)  # Get predictions
        
        # Process results
        current_frame_objects = set()
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)
            
            for box, conf, cls_id in zip(boxes, confidences, class_ids):
                if conf > 0.5:  # Confidence threshold
                    x1, y1, x2, y2 = map(int, box)
                    label = classes[cls_id]
                    
                    # Draw bounding box
                    color = (0, 255, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
                    current_frame_objects.add(label.lower())

        # Check for new objects and save them
        new_objects = current_frame_objects - detected_objects
        if new_objects:
            detected_objects.update(new_objects)
            if save_detections(new_objects):
                print(f"New detections saved: {new_objects}")

        # Display frame
        cv2.imshow("Object Detection", frame)

        # Exit conditions
        if cv2.getWindowProperty("Object Detection", cv2.WND_PROP_VISIBLE) < 1:
            print("Window closed by user.")
            break

        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:  # 27 is the ESC key
            print("Exit key pressed.")
            break
finally:
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()