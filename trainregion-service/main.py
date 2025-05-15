import os
from pathlib import Path
from ultralytics import YOLO

# Kiểm tra xem model đã tồn tại chưa
model_path = "yolov8x.pt"
if not os.path.exists(model_path):
    print(f"Model {model_path} không tồn tại. Đang tải xuống...")
    # YOLO sẽ tự động tải model nếu không tìm thấy

# Load a COCO-pretrained YOLOv8x model
model = YOLO(model_path)
print(f"Đã tải model {model_path} thành công!")

# Train the model on the dataset
print("Bắt đầu huấn luyện model...")
results = model.train(data="mydata.yaml", epochs=20)
print("Huấn luyện hoàn tất!")

# Đường dẫn đến model đã huấn luyện
best_model_path = Path("runs/detect/train/weights/best.pt")
if best_model_path.exists():
    print(f"Model đã huấn luyện được lưu tại: {best_model_path}")

    # Chạy inference với model đã huấn luyện (bỏ comment nếu muốn sử dụng)
    # test_image = "path/to/test_image.jpg"
    # if os.path.exists(test_image):
    #     print(f"Đang chạy inference trên ảnh {test_image}...")
    #     results = model(test_image)
    #     print("Inference hoàn tất!")