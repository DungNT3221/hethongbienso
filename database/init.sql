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
