# API Gateway

API Gateway cho hệ thống quản lý biển số xe.

## Chức năng

- Điểm vào duy nhất cho frontend
- Chuyển tiếp các yêu cầu đến các service tương ứng
- Xác thực JWT token

## Cài đặt và chạy

### Sử dụng Docker

```bash
# Build image
docker build -t api-gateway .

# Chạy container
docker run -p 3000:3000 \
  -e AUTH_SERVICE_URL=http://localhost:3001 \
  -e VEHICLE_SERVICE_URL=http://localhost:3002 \
  -e JWT_SECRET=your_jwt_secret_key \
  api-gateway
```

### Sử dụng Node.js

```bash
# Cài đặt dependencies
npm install

# Chạy service
npm start
```

## API

API Gateway chuyển tiếp các yêu cầu đến các service tương ứng:

### Auth Service

- POST /api/auth/login
- GET /api/auth/me
- GET /api/auth/verify

### Vehicle Service

- GET /api/vehicles
- GET /api/vehicles/:id
- GET /api/vehicles/plate/:licensePlate
- POST /api/vehicles
- PUT /api/vehicles/:id
- DELETE /api/vehicles/:id

## Cấu hình

API Gateway sử dụng các biến môi trường sau:

- `AUTH_SERVICE_URL`: URL của Auth Service
- `VEHICLE_SERVICE_URL`: URL của Vehicle Service
- `JWT_SECRET`: Khóa bí mật để xác thực JWT token
- `PORT`: Cổng để chạy API Gateway (mặc định: 3000)
