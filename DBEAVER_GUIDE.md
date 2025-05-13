# Hướng dẫn kết nối với MySQL bằng DBeaver

## 1. Cài đặt DBeaver

1. Tải DBeaver từ [trang chủ DBeaver](https://dbeaver.io/download/)
2. Cài đặt DBeaver theo hướng dẫn

## 2. Khởi động Docker Compose

Trước khi kết nối với DBeaver, bạn cần khởi động các container MySQL bằng Docker Compose:

```bash
docker-compose up -d auth-db vehicle-db
```

Lệnh này sẽ khởi động 2 container MySQL:

- `auth-db`: Cơ sở dữ liệu cho Auth Service, chạy trên cổng 3306
- `vehicle-db`: Cơ sở dữ liệu cho Vehicle Service, chạy trên cổng 3307

## 3. Kết nối với Auth Database

1. Mở DBeaver
2. Nhấp chuột phải vào Database Navigator, chọn "Create" > "Connection"
3. Chọn "MySQL"
4. Nhập thông tin kết nối:
   - Server Host: localhost
   - Port: 13306
   - Database: auth_db
   - Username: auth_user
   - Password: 123456
5. Nhấp "Test Connection" để kiểm tra kết nối
6. Nhấp "Finish" để tạo kết nối

## 4. Kết nối với Vehicle Database

1. Mở DBeaver
2. Nhấp chuột phải vào Database Navigator, chọn "Create" > "Connection"
3. Chọn "MySQL"
4. Nhập thông tin kết nối:
   - Server Host: localhost
   - Port: 13307
   - Database: vehicle_db
   - Username: vehicle_user
   - Password: 123456
5. Nhấp "Test Connection" để kiểm tra kết nối
6. Nhấp "Finish" để tạo kết nối

## 5. Xem và quản lý dữ liệu

Sau khi kết nối thành công, bạn có thể:

1. Xem cấu trúc bảng:

   - Mở rộng kết nối > Schemas > auth_db/vehicle_db > Tables
   - Nhấp đúp vào bảng để xem cấu trúc

2. Xem dữ liệu:

   - Nhấp chuột phải vào bảng, chọn "View Data"

3. Thực thi truy vấn SQL:
   - Nhấp chuột phải vào kết nối, chọn "SQL Editor" > "Open SQL Editor"
   - Nhập truy vấn SQL và nhấp "Execute SQL Statement" (Ctrl+Enter)

## 6. Các truy vấn SQL hữu ích

### Auth Database

```sql
-- Xem tất cả người dùng
SELECT * FROM users;

-- Thêm người dùng mới
INSERT INTO users (username, password, role, fullName)
VALUES ('newuser', '$2a$10$eCwRmT/YRBGgG.FP.y3ZB.eBGq0KUScMGEd02Cj.HPqh5jQZKmXSK', 'police', 'New User');

-- Cập nhật người dùng
UPDATE users SET fullName = 'Updated Name' WHERE username = 'newuser';

-- Xóa người dùng
DELETE FROM users WHERE username = 'newuser';
```

### Vehicle Database

```sql
-- Xem tất cả xe
SELECT * FROM vehicles;

-- Thêm xe mới
INSERT INTO vehicles (licensePlate, ownerName, ownerID, vehicleType, brand, model, color, registrationDate, expiryDate, status)
VALUES ('99A-12345', 'Nguyễn Văn X', '001234567899', 'Sedan', 'Toyota', 'Vios', 'Trắng', '2023-01-15', '2028-01-15', 'active');

-- Cập nhật xe
UPDATE vehicles SET color = 'Đen' WHERE licensePlate = '99A-12345';

-- Xóa xe
DELETE FROM vehicles WHERE licensePlate = '99A-12345';

-- Tìm xe theo biển số
SELECT * FROM vehicles WHERE licensePlate LIKE '%12345%';
```

## 7. Xử lý sự cố

### Không thể kết nối với cơ sở dữ liệu

1. Kiểm tra xem các container MySQL đã chạy chưa:

```bash
docker ps
```

2. Nếu container không chạy, khởi động lại:

```bash
docker-compose up -d auth-db vehicle-db
```

3. Kiểm tra logs của container:

```bash
docker logs auth-db
docker logs vehicle-db
```

### Lỗi "Access denied"

1. Kiểm tra thông tin đăng nhập:

   - Username: auth_user/vehicle_user
   - Password: 123456

2. Nếu vẫn gặp lỗi, thử kết nối với tài khoản root:

   - Username: root
   - Password: root

3. Nếu gặp lỗi "Access denied for user 'auth_user'@'172.18.0.1'", hãy thử thay đổi Server Host:
   - Thay vì sử dụng "localhost", hãy sử dụng "127.0.0.1"
   - Hoặc sử dụng IP của Docker container: "172.17.0.1" hoặc "host.docker.internal"
     docker exec -it vehicle-db mysql -uroot -proot -e "ALTER USER 'vehicle_user'@'%' IDENTIFIED WITH mysql_native_password BY '123456';"

docker exec -it vehicle-db mysql -uroot -proot -e "FLUSH PRIVILEGES;"
