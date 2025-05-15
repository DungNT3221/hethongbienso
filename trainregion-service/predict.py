from ultralytics import YOLO
from PIL import Image

# Load a COCO-pretrained YOLOv8n model
model = YOLO(r".\runs\detect\train2\weights\best.pt")

# Run inference with the YOLOv8n model on the image
results = model(r"./image.png", conf=0.9)

# Results
for r in results:
    # Print number of detected boxes
    print(f"Detected {len(r.boxes)} license plates")

    # Print all box coordinates
    for i in range(len(r.boxes)):
        box = r.boxes[i]
        print(f"Box {i+1}: {box.xyxy[0].tolist()} - Confidence: {box.conf[0].item():.2f}")

    # Plot results
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    im.save("result.png")  # save image
