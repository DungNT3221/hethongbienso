-- Tạo database
CREATE DATABASE IF NOT EXISTS trainregion_db;
USE trainregion_db;

-- Bảng models lưu thông tin các model đã train
CREATE TABLE IF NOT EXISTS models (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type ENUM('yolov8n', 'yolov8s', 'yolov8m', 'yolov8l', 'yolov8x') NOT NULL,
    version VARCHAR(20) NOT NULL,
    epochs INT NOT NULL,
    batch_size INT NOT NULL,
    dataset_size INT NOT NULL,
    training_time FLOAT NOT NULL,
    map50 FLOAT,
    map95 FLOAT,
    model_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng train_jobs lưu thông tin các job train model
CREATE TABLE IF NOT EXISTS train_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_id INT,
    status ENUM('pending', 'running', 'completed', 'failed', 'stopped') NOT NULL DEFAULT 'pending',
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES models(id)
);

-- XÓA BẢNG predict_logs - không cần thiết cho trainregion service
-- Trainregion chỉ tập trung vào training, không prediction

-- Bảng datasets lưu thông tin dataset upload
CREATE TABLE IF NOT EXISTS datasets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    upload_path VARCHAR(500) NOT NULL,
    image_count INT DEFAULT 0,
    file_size BIGINT DEFAULT 0,
    upload_type ENUM('zip', 'images') DEFAULT 'images',
    has_labels BOOLEAN DEFAULT FALSE,
    labeling_method ENUM('manual', 'auto', 'template') DEFAULT 'auto',
    labeling_accuracy FLOAT DEFAULT 0.0,
    status ENUM('uploaded', 'processing', 'ready', 'error') DEFAULT 'uploaded',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Cập nhật bảng models thêm approval workflow và dataset reference
ALTER TABLE models ADD COLUMN is_approved BOOLEAN DEFAULT FALSE;
ALTER TABLE models ADD COLUMN approval_notes TEXT;
ALTER TABLE models ADD COLUMN dataset_id INT;
ALTER TABLE models ADD COLUMN train_val_split FLOAT DEFAULT 0.8;
ALTER TABLE models ADD FOREIGN KEY (dataset_id) REFERENCES datasets(id);

-- Cập nhật bảng train_jobs thêm thông tin training chi tiết
ALTER TABLE train_jobs ADD COLUMN name VARCHAR(255);
ALTER TABLE train_jobs ADD COLUMN dataset_id INT;
ALTER TABLE train_jobs ADD COLUMN model_type ENUM('yolov8n', 'yolov8s', 'yolov8m', 'yolov8l', 'yolov8x') DEFAULT 'yolov8n';
ALTER TABLE train_jobs ADD COLUMN epochs INT DEFAULT 100;
ALTER TABLE train_jobs ADD COLUMN batch_size INT DEFAULT 16;
ALTER TABLE train_jobs ADD COLUMN learning_rate FLOAT DEFAULT 0.01;
ALTER TABLE train_jobs ADD COLUMN image_size INT DEFAULT 640;
ALTER TABLE train_jobs ADD COLUMN progress FLOAT DEFAULT 0.0;
ALTER TABLE train_jobs ADD COLUMN current_epoch INT DEFAULT 0;
ALTER TABLE train_jobs ADD COLUMN best_map50 FLOAT DEFAULT 0.0;
ALTER TABLE train_jobs ADD COLUMN best_map95 FLOAT DEFAULT 0.0;
ALTER TABLE train_jobs ADD COLUMN training_time FLOAT DEFAULT 0.0;
ALTER TABLE train_jobs ADD COLUMN result_path VARCHAR(500);
ALTER TABLE train_jobs ADD FOREIGN KEY (dataset_id) REFERENCES datasets(id);

-- Thêm các trường mới cho stop training functionality
ALTER TABLE train_jobs ADD COLUMN can_stop BOOLEAN DEFAULT TRUE;
ALTER TABLE train_jobs ADD COLUMN stop_requested BOOLEAN DEFAULT FALSE;
ALTER TABLE train_jobs ADD COLUMN stopped_at TIMESTAMP NULL;

-- Status enum đã được cập nhật ở trên để bao gồm 'stopped'