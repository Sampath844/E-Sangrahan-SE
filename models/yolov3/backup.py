import cv2
import numpy as np

# Load pre-trained YOLO model
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Open the video capture object for the laptop camera (usually index 0)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame and check if it's successful
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Set up the input blob for the network
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1/255.0, size=(416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)

    # Get output layer names and run forward pass to get detections
    output_layer_names = net.getUnconnectedOutLayersNames()
    outs = net.forward(output_layer_names)

    # Initialize lists for detected class IDs, confidences, and bounding boxes
    class_ids = []
    confidences = []
    boxes = []

    # Process detections from each output layer
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Filter out weak detections by confidence threshold
            if confidence > 0.5:
                # Scale the bounding box coordinates to the original image dimensions
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # Apply non-maximum suppression to remove redundant overlapping boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw bounding boxes on the frame if there are any detections
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            label = classes[class_ids[i]]
            confidence = confidences[i]
            color = (0, 255, 0)  # Green bounding box color
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display the resulting frame
    cv2.imshow("Object Detection", frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
