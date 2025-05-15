# TrainRegion Service

TrainRegion Service là một microservice trong hệ thống quản lý biển số xe, có nhiệm vụ huấn luyện mô hình YOLOv8 để nhận dạng vùng chứa biển số xe trong ảnh.

## Cài đặt

### Yêu cầu

- Python 3.8 hoặc mới hơn
- CUDA (nếu muốn sử dụng GPU)
- Label Studio (cho việc annotation dữ liệu)

### Thiết lập môi trường

1. Chạy script `setup_env.bat` để tạo môi trường ảo và cài đặt các thư viện cần thiết:

```bash
setup_env.bat
```

2. Kích hoạt môi trường ảo:

```bash
call venv\Scripts\activate
```

## Sử dụng Label Studio

### Khởi động Label Studio

```bash
start_label_studio.bat
```

Hoặc:

```bash
call venv\Scripts\activate
label-studio start
```

Label Studio sẽ chạy tại http://localhost:8082. Đăng nhập và tạo một API key từ giao diện người dùng.

### Cấu hình Label Studio

1. Sau khi đăng nhập, tạo một project mới
2. Chọn "Object Detection with Bounding Boxes" làm template
3. Thêm label "license_plate"
4. Tải lên ảnh để annotation

### Lấy API key

1. Vào "Account & Settings" (góc trên bên phải)
2. Chọn tab "Access Token"
3. Tạo token mới
4. Sao chép token và thêm vào file `.env`:

```
LABEL_STUDIO_API_KEY=your_api_key_here
```

## Kết nối với Label Studio

Sử dụng script `label_studio_connector.py` để tương tác với Label Studio:

```bash
# Liệt kê tất cả các project
python src/python/label_studio_connector.py list-projects

# Tạo project mới
python src/python/label_studio_connector.py create-project --title "License Plate Detection"

# Tải lên ảnh
python src/python/label_studio_connector.py upload-images --project-id 1 --image-dir path/to/images

# Xuất annotations
python src/python/label_studio_connector.py export-annotations --project-id 1 --export-dir path/to/export --format YOLO
```

## Huấn luyện mô hình YOLOv8

Sau khi đã có dữ liệu được annotation, bạn có thể huấn luyện mô hình YOLOv8:

```bash
python src/python/train_yolov8.py --data-dir path/to/dataset --output-dir path/to/output --model-size n --epochs 100
```

Tham số:

- `--data-dir`: Thư mục chứa dữ liệu (phải có cấu trúc train/val)
- `--output-dir`: Thư mục để lưu kết quả
- `--model-size`: Kích thước mô hình (n, s, m, l, x)
- `--epochs`: Số epoch huấn luyện
- `--batch-size`: Kích thước batch
- `--img-size`: Kích thước ảnh đầu vào
- `--no-pretrained`: Không sử dụng pretrained weights
- `--device`: Thiết bị để huấn luyện (cuda, cpu)

## Sử dụng Docker

Bạn có thể sử dụng Docker để chạy TrainRegion Service:

```bash
# Build image
docker build -t trainregion-service .

# Chạy container
docker run -p 3003:3003 -v $(pwd)/data:/app/data trainregion-service
```

## Tích hợp với hệ thống

TrainRegion Service được thiết kế để tích hợp với hệ thống quản lý biển số xe hiện tại. Để tích hợp:

1. Cập nhật file `docker-compose.yml` để thêm TrainRegion Service
2. Cập nhật API Gateway để chuyển tiếp các yêu cầu đến TrainRegion Service
3. Sử dụng Auth Service hiện tại để xác thực người dùng

## Cấu trúc thư mục

- `src/python/`: Mã nguồn Python cho việc huấn luyện và đánh giá mô hình
- `src/api/`: API endpoints
- `src/models/`: Định nghĩa các model database
- `src/services/`: Business logic
- `data/`: Thư mục chứa dữ liệu, mô hình và kết quả
- `venv/`: Môi trường ảo Python

## Tài liệu tham khảo

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [Label Studio Documentation](https://labelstud.io/guide/)
