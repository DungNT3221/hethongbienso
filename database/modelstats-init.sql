-- Tạo database cho Model Statistics Service (Đơn giản hóa)
CREATE DATABASE IF NOT EXISTS modelstats_db;
USE modelstats_db;

-- Bảng training_history lưu lịch sử training từ trainregion service
CREATE TABLE IF NOT EXISTS training_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_id INT,
    model_name VARCHAR(255) NOT NULL,
    model_type ENUM('yolov8n', 'yolov8s', 'yolov8m', 'yolov8l', 'yolov8x') NOT NULL,
    dataset_name VARCHAR(255),
    dataset_size INT DEFAULT 0,
    epochs INT,
    batch_size INT,
    learning_rate FLOAT,
    training_time FLOAT, -- Thời gian training (giây)
    map50 FLOAT,
    map95 FLOAT,
    status ENUM('completed', 'failed', 'stopped') NOT NULL,
    is_approved BOOLEAN DEFAULT FALSE,
    model_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tạo indexes để tối ưu performance
CREATE INDEX idx_training_history_created_at ON training_history(created_at);
CREATE INDEX idx_training_history_model_type ON training_history(model_type);
CREATE INDEX idx_training_history_status ON training_history(status);
CREATE INDEX idx_training_history_map50 ON training_history(map50);

-- Tạo view để dễ dàng truy vấn thống kê tổng quan
CREATE VIEW v_model_stats_summary AS
SELECT
    COUNT(*) as total_models,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_models,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_models,
    COUNT(CASE WHEN status = 'stopped' THEN 1 END) as stopped_models,
    ROUND(AVG(CASE WHEN status = 'completed' THEN map50 END), 3) as avg_map50,
    ROUND(AVG(CASE WHEN status = 'completed' THEN map95 END), 3) as avg_map95,
    ROUND(AVG(CASE WHEN status = 'completed' THEN training_time END), 2) as avg_training_time,
    ROUND(MAX(map50), 3) as best_map50,
    ROUND(MAX(map95), 3) as best_map95,
    ROUND((COUNT(CASE WHEN status = 'completed' THEN 1 END) * 100.0 / COUNT(*)), 1) as success_rate
FROM training_history;

-- Tạo view cho top models (hiệu suất cao nhất)
CREATE VIEW v_top_models AS
SELECT
    model_id,
    model_name,
    model_type,
    map50,
    map95,
    training_time,
    dataset_size,
    epochs,
    is_approved,
    created_at,
    ROUND((map50 * 0.7 + map95 * 0.3), 3) as composite_score
FROM training_history
WHERE status = 'completed'
ORDER BY composite_score DESC
LIMIT 10;

-- Tạo view cho thống kê theo loại model
CREATE VIEW v_model_type_stats AS
SELECT
    model_type,
    COUNT(*) as total_count,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_count,
    ROUND(AVG(CASE WHEN status = 'completed' THEN map50 END), 3) as avg_map50,
    ROUND(MAX(map50), 3) as best_map50,
    ROUND(AVG(CASE WHEN status = 'completed' THEN training_time END), 2) as avg_training_time
FROM training_history
GROUP BY model_type
ORDER BY avg_map50 DESC;
