import os
from pathlib import Path
from ultralytics import YOLO

# Load a COCO-pretrained YOLOv8n model
# model = YOLO("yolov8n.pt")

# Train the model using the 'coco8.yaml' dataset for 5 epochs
# results = model.train(data="coco8.yaml", epochs=5)

# Load a COCO-pretrained YOLOv8x model
model = YOLO("yolov8n.pt")

# Train the model using the 'mydata.yaml' dataset for 5 epochs
results = model.train(data="mydata.yaml", epochs=5)
