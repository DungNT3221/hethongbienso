from ultralytics import YOLO

# Load a COCO-pretrained YOLOv8n model
model = YOLO("yolov8x.pt")


# Train the model on the COCO8 example dataset for 20 epochs
results = model.train(data="mydata.yaml", epochs=20)

# Run inference with the YOLOv8n model on the 'bus.jpg' image
# results = model("path/to/bus.jpg")