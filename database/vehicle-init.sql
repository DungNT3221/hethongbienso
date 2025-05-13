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
