# Hướng dẫn kết nối với MySQL trong hệ thống microservice

## 1. Cài đặt MySQL

### Windows

1. Tải MySQL Installer từ [trang chủ MySQL](https://dev.mysql.com/downloads/installer/)
2. Chạy installer và làm theo hướng dẫn cài đặt
3. Trong quá trình cài đặt, đặt mật khẩu cho tài khoản root
4. Sau khi cài đặt, mở MySQL Command Line Client để kiểm tra kết nối

### Linux (Ubuntu)

```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

### macOS

```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

## 2. Tạo cơ sở dữ liệu và bảng

Chạy script SQL trong file `database/init.sql` để tạo cơ sở dữ liệu và bảng:

```bash
mysql -u root -p < database/init.sql
```

Hoặc mở MySQL Command Line Client và chạy các lệnh SQL sau:

```sql
-- Tạo cơ sở dữ liệu cho Auth Service
CREATE DATABASE IF NOT EXISTS auth_db;
USE auth_db;

-- Tạo bảng users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'police') NOT NULL,
    fullName VARCHAR(100) NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Thêm dữ liệu mẫu cho bảng users
-- Mật khẩu: admin123 và police123 (đã được hash)
INSERT INTO users (username, password, role, fullName) VALUES
('admin', '$2a$10$eCwRmT/YRBGgG.FP.y3ZB.eBGq0KUScMGEd02Cj.HPqh5jQZKmXSK', 'admin', 'System Administrator'),
('police', '$2a$10$xLCRbKpnYQJGq0oe.KZ8s.KK.LUFEFZpKZwVGR9KgE4qIEsOvzTlW', 'police', 'Police Officer');

-- Tạo cơ sở dữ liệu cho Vehicle Service
CREATE DATABASE IF NOT EXISTS vehicle_db;
USE vehicle_db;

-- Tạo bảng vehicles
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    licensePlate VARCHAR(20) NOT NULL UNIQUE,
    ownerName VARCHAR(100) NOT NULL,
    ownerID VARCHAR(20) NOT NULL,
    vehicleType VARCHAR(50) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    color VARCHAR(30) NOT NULL,
    registrationDate DATE NOT NULL,
    expiryDate DATE NOT NULL,
    status ENUM('active', 'expired', 'suspended') NOT NULL DEFAULT 'active',
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Thêm dữ liệu mẫu cho bảng vehicles
INSERT INTO vehicles (licensePlate, ownerName, ownerID, vehicleType, brand, model, color, registrationDate, expiryDate, status) VALUES
('29A-12345', 'Nguyễn Văn A', '001234567890', 'Sedan', 'Toyota', 'Camry', 'Đen', '2022-01-15', '2027-01-15', 'active'),
('30A-54321', 'Trần Thị B', '001234567891', 'SUV', 'Honda', 'CR-V', 'Trắng', '2021-05-20', '2026-05-20', 'active'),
('31A-98765', 'Lê Văn C', '001234567892', 'Hatchback', 'Mazda', 'Mazda3', 'Đỏ', '2020-11-10', '2025-11-10', 'active');
```

## 3. Cấu hình các dịch vụ để kết nối với MySQL

### Auth Service

Cập nhật file `.env` trong thư mục `auth-service`:

```
PORT=3001
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=auth_db
JWT_SECRET=your_jwt_secret_key
```

### Vehicle Service

Cập nhật file `.env` trong thư mục `vehicle-service`:

```
PORT=3002
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=vehicle_db
JWT_SECRET=your_jwt_secret_key
AUTH_SERVICE_URL=http://localhost:3001
```

## 4. Cập nhật frontend để kết nối với API

Frontend kết nối với backend thông qua API Gateway. Các API được định nghĩa trong file `frontend/js/api.js`.

Đảm bảo rằng biến `API_URL` trong file `frontend/js/api.js` trỏ đến API Gateway:

```javascript
const API_URL = 'http://localhost:3000/api';
```

## 5. Chạy hệ thống

1. Chạy Auth Service:
```bash
cd auth-service
npm start
```

2. Chạy Vehicle Service:
```bash
cd vehicle-service
npm start
```

3. Chạy API Gateway:
```bash
cd api-gateway
npm start
```

4. Chạy Frontend:
```bash
cd frontend
python -m http.server 8080
```

5. Truy cập ứng dụng tại http://localhost:8080/redirect.html

## 6. Xử lý lỗi khi click edit vehicle

Nếu bạn gặp lỗi "Hmmm... can't reach this page" khi click vào nút Edit, hãy kiểm tra các điểm sau:

1. Đảm bảo đường dẫn trong file `dashboard.html` đúng:
```javascript
window.location.href = `mock-add-vehicle.html?id=${id}`;
```

2. Đảm bảo file `mock-add-vehicle.html` tồn tại trong thư mục `frontend`

3. Kiểm tra console của trình duyệt để xem có lỗi JavaScript nào không
