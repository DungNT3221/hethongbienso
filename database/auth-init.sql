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
