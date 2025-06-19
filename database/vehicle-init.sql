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
('31A-98765', 'Lê Văn C', '001234567892', 'Hatchback', 'Mazda', 'Mazda3', 'Đỏ', '2020-11-10', '2025-11-10', 'active'),
('32A-11111', 'Phạm Văn D', '001234567893', 'Sedan', 'Hyundai', 'Elantra', 'Xanh', '2023-03-12', '2028-03-12', 'active'),
('33A-22222', 'Hoàng Thị E', '001234567894', 'SUV', 'Ford', 'EcoSport', 'Bạc', '2022-07-08', '2027-07-08', 'active'),
('34A-33333', 'Vũ Văn F', '001234567895', 'Pickup', 'Isuzu', 'D-Max', 'Xám', '2021-12-25', '2026-12-25', 'active'),
('35A-44444', 'Đặng Thị G', '001234567896', 'Hatchback', 'Kia', 'Morning', 'Vàng', '2023-01-30', '2028-01-30', 'active'),
('36A-55555', 'Bùi Văn H', '001234567897', 'Sedan', 'Nissan', 'Sunny', 'Tím', '2022-09-14', '2027-09-14', 'expired'),
('37A-66666', 'Lý Thị I', '001234567898', 'SUV', 'Mitsubishi', 'Outlander', 'Nâu', '2020-04-18', '2025-04-18', 'active'),
('38A-77777', 'Cao Văn K', '001234567899', 'Sedan', 'Volkswagen', 'Jetta', 'Cam', '2023-06-22', '2028-06-22', 'suspended');
