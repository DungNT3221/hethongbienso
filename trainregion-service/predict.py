from ultralytics import YOLO
from PIL import Image
import os

# Lấy đường dẫn thư mục hiện tại của script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load a COCO-pretrained YOLOv8n model
model_path = os.path.join(script_dir, "runs", "detect", "train2", "weights", "best.pt")
model = YOLO(model_path)

# Run inference with the YOLOv8n model on the image
image_path = os.path.join(script_dir, "image.png")
results = model(image_path, conf=0.9)

# Results
for r in results:
    if r.boxes:
        print(f"Detected {len(r.boxes)} license plates")

        # Lưu ảnh kết quả
        im_array = r.plot()
        im = Image.fromarray(im_array[..., ::-1])
        result_path = os.path.join(script_dir, "result.png")
        im.save(result_path)
        print(f"Result saved to: {result_path}")
    else:
        print("No license plate detected.")
