# Vehicle Service

Vehicle Service cho hệ thống quản lý biển số xe.

## Chức năng

- Quản lý thông tin đăng ký xe (CRUD)
- Tìm kiếm xe theo biển số
- Kiểm tra trạng thái xe (active, expired, suspended)

## Cài đặt và chạy

### Sử dụng Docker

```bash
# Build image
docker build -t vehicle-service .

# Chạy container
docker run -p 3002:3002 \
  -e DB_HOST=localhost \
  -e DB_PORT=3306 \
  -e DB_USER=vehicle_user \
  -e DB_PASSWORD=vehicle_password \
  -e DB_NAME=vehicle_db \
  -e JWT_SECRET=your_jwt_secret_key \
  -e AUTH_SERVICE_URL=http://localhost:3001 \
  vehicle-service
```

### Sử dụng Node.js

```bash
# Cài đặt dependencies
npm install

# Chạy service
npm start
```

## API

### GET /api/vehicles

Lấy danh sách tất cả các xe.

**Headers:**

```
x-auth-token: jwt_token
```

**Response:**

```json
[
  {
    "id": "1",
    "licensePlate": "29A-12345",
    "ownerName": "Nguyễn Văn A",
    "ownerID": "001234567890",
    "vehicleType": "Sedan",
    "brand": "Toyota",
    "model": "Camry",
    "color": "Đen",
    "registrationDate": "2022-01-15",
    "expiryDate": "2027-01-15",
    "status": "active"
  },
  ...
]
```

### GET /api/vehicles/:id

Lấy thông tin xe theo ID.

**Headers:**

```
x-auth-token: jwt_token
```

**Response:**

```json
{
  "id": "1",
  "licensePlate": "29A-12345",
  "ownerName": "Nguyễn Văn A",
  "ownerID": "001234567890",
  "vehicleType": "Sedan",
  "brand": "Toyota",
  "model": "Camry",
  "color": "Đen",
  "registrationDate": "2022-01-15",
  "expiryDate": "2027-01-15",
  "status": "active"
}
```

### GET /api/vehicles/plate/:licensePlate

Tìm xe theo biển số.

**Headers:**

```
x-auth-token: jwt_token
```

**Response:**

```json
{
  "id": "1",
  "licensePlate": "29A-12345",
  "ownerName": "Nguyễn Văn A",
  "ownerID": "001234567890",
  "vehicleType": "Sedan",
  "brand": "Toyota",
  "model": "Camry",
  "color": "Đen",
  "registrationDate": "2022-01-15",
  "expiryDate": "2027-01-15",
  "status": "active"
}
```

### POST /api/vehicles

Tạo xe mới.

**Headers:**

```
x-auth-token: jwt_token
Content-Type: application/json
```

**Request:**

```json
{
  "licensePlate": "29A-12345",
  "ownerName": "Nguyễn Văn A",
  "ownerID": "001234567890",
  "vehicleType": "Sedan",
  "brand": "Toyota",
  "model": "Camry",
  "color": "Đen",
  "registrationDate": "2022-01-15",
  "expiryDate": "2027-01-15",
  "status": "active"
}
```

**Response:**

```json
{
  "id": "1",
  "licensePlate": "29A-12345",
  "ownerName": "Nguyễn Văn A",
  "ownerID": "001234567890",
  "vehicleType": "Sedan",
  "brand": "Toyota",
  "model": "Camry",
  "color": "Đen",
  "registrationDate": "2022-01-15",
  "expiryDate": "2027-01-15",
  "status": "active"
}
```

### PUT /api/vehicles/:id

Cập nhật thông tin xe.

**Headers:**

```
x-auth-token: jwt_token
Content-Type: application/json
```

**Request:**

```json
{
  "color": "Trắng"
}
```

**Response:**

```json
{
  "id": "1",
  "licensePlate": "29A-12345",
  "ownerName": "Nguyễn Văn A",
  "ownerID": "001234567890",
  "vehicleType": "Sedan",
  "brand": "Toyota",
  "model": "Camry",
  "color": "Trắng",
  "registrationDate": "2022-01-15",
  "expiryDate": "2027-01-15",
  "status": "active"
}
```

### DELETE /api/vehicles/:id

Xóa xe.

**Headers:**

```
x-auth-token: jwt_token
```

**Response:**

```json
{
  "message": "Vehicle deleted successfully"
}
```
