# Auth Service

Auth Service cho hệ thống quản lý biển số xe.

## Chức năng

- Đăng nhập và xác thực người dùng
- Quản lý phân quyền (admin, police)
- Tạo và xác thực JWT token

## Cài đặt và chạy

### Sử dụng Docker

```bash
# Build image
docker build -t auth-service .

# Chạy container
docker run -p 3001:3001 \
  -e DB_HOST=localhost \
  -e DB_PORT=3306 \
  -e DB_USER=auth_user \
  -e DB_PASSWORD=auth_password \
  -e DB_NAME=auth_db \
  -e JWT_SECRET=your_jwt_secret_key \
  auth-service
```

### Sử dụng Node.js

```bash
# Cài đặt dependencies
npm install

# Chạy service
npm start
```

## API

### POST /api/auth/login

Đăng nhập và lấy JWT token.

**Request:**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**

```json
{
  "token": "jwt_token",
  "user": {
    "id": "1",
    "username": "admin",
    "role": "admin",
    "fullName": "System Administrator"
  }
}
```

### GET /api/auth/me

Lấy thông tin người dùng hiện tại.

**Headers:**

```
x-auth-token: jwt_token
```

**Response:**

```json
{
  "id": "1",
  "username": "admin",
  "role": "admin",
  "fullName": "System Administrator"
}
```

### GET /api/auth/verify

Xác thực JWT token.

**Headers:**

```
x-auth-token: jwt_token
```

**Response:**

```json
{
  "valid": true,
  "user": {
    "id": "1",
    "username": "admin",
    "role": "admin"
  }
}
```
