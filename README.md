# Hệ thống quản lý biển số xe

Hệ thống quản lý biển số xe là một ứng dụng microservice cho phép quản lý thông tin đăng ký xe và phát hiện vi phạm biển số.

## Cấu trúc hệ thống

Hệ thống bao gồm các thành phần sau:

- **Auth Service**: Quản lý xác thực người dùng
- **Vehicle Service**: Quản lý thông tin đăng ký xe
- **API Gateway**: Điểm vào duy nhất cho frontend
- **Frontend**: Giao diện người dùng
- **Database**: MySQL cho lưu trữ dữ liệu

## Cài đặt và chạy hệ thống

### Yêu cầu

- Docker và Docker Compose
- DBeaver (tùy chọn, để quản lý cơ sở dữ liệu)

### Chạy hệ thống

1. Clone repository:

```bash
git clone <repository-url>
cd hethongbienso
```

2. Khởi động hệ thống bằng Docker Compose:

```bash
docker-compose up -d
```

Hoặc sử dụng file run.bat:

```bash
run.bat
```

3. Truy cập ứng dụng tại: http://localhost:8080

### Dừng hệ thống

```bash
docker-compose down
```

### Kết nối với cơ sở dữ liệu

Xem hướng dẫn chi tiết trong file [DBEAVER_GUIDE.md](DBEAVER_GUIDE.md).

### Cấu trúc cơ sở dữ liệu

1. **Auth Database (auth_db)**:

   - Bảng `users`: Lưu trữ thông tin người dùng (admin, police)

2. **Vehicle Database (vehicle_db)**:
   - Bảng `vehicles`: Lưu trữ thông tin đăng ký xe

## Tài khoản demo

- **Admin**:

  - Username: admin
  - Password: admin123

- **Police**:
  - Username: police
  - Password: police123

## API Endpoints

### Auth Service (http://localhost:3001)

- `POST /api/auth/login`: Đăng nhập và lấy token
- `GET /api/auth/me`: Lấy thông tin người dùng hiện tại
- `GET /api/auth/verify`: Xác thực token

### Vehicle Service (http://localhost:3002)

- `GET /api/vehicles`: Lấy danh sách xe
- `GET /api/vehicles/:id`: Lấy thông tin xe theo ID
- `GET /api/vehicles/plate/:licensePlate`: Lấy thông tin xe theo biển số
- `POST /api/vehicles`: Tạo mới thông tin xe
- `PUT /api/vehicles/:id`: Cập nhật thông tin xe
- `DELETE /api/vehicles/:id`: Xóa thông tin xe

## Tài liệu

Xem thêm tài liệu chi tiết tại thư mục `docs/`.
