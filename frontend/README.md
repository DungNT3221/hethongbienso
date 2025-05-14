# Frontend Service

Frontend service cho hệ thống quản lý biển số xe.

## Cấu trúc thư mục

- `index.html`: Trang chủ, chuyển hướng đến trang đăng nhập hoặc dashboard
- `login.html`: Trang đăng nhập
- `dashboard.html`: Trang quản lý danh sách xe
- `add-vehicle.html`: Trang thêm/sửa thông tin xe
- `js/api.js`: API client để kết nối với backend
- `js/mock-api.js`: Mock API để frontend có thể hoạt động độc lập

## Cài đặt và chạy

### Sử dụng Docker

```bash
# Build image
docker build -t frontend .

# Chạy container
docker run -p 8080:80 frontend
```

### Sử dụng Nginx

```bash
# Cài đặt Nginx
# Sao chép các file vào thư mục /usr/share/nginx/html
# Khởi động Nginx
```

### Sử dụng Python (cho phát triển)

```bash
# Chạy server HTTP đơn giản
python -m http.server 8080
```

## API

Frontend kết nối với backend thông qua API Gateway. Các API được định nghĩa trong file `js/api.js`.

### Chuyển từ Mock API sang API thật

Để chuyển từ Mock API sang API thật, bạn cần thay đổi script trong các file HTML:

```html
<!-- Thay đổi từ -->
<script src="js/mock-api.js"></script>

<!-- Thành -->
<script src="js/api.js"></script>
```
