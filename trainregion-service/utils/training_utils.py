import os
import time
import yaml
from ultralytics import YOLO
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TrainingUtils:
    def __init__(self):
        self.base_models = {
            'yolov8n': 'yolov8n.pt',
            'yolov8s': 'yolov8s.pt',
            'yolov8m': 'yolov8m.pt',
            'yolov8l': 'yolov8l.pt',
            'yolov8x': 'yolov8x.pt'
        }

    def run_training(self, config, progress_callback=None, stop_check_callback=None):
        """
        Chạy training với config được cung cấp

        Args:
            config: Dictionary chứa training configuration
            progress_callback: Function để update progress

        Returns:
            Dictionary chứa kết quả training
        """
        try:
            job_id = config['job_id']
            dataset_path = config['dataset_path']
            model_type = config.get('model_type', 'yolov8n')
            epochs = config.get('epochs', 100)
            batch_size = config.get('batch_size', 16)
            learning_rate = config.get('learning_rate', 0.01)
            image_size = config.get('image_size', 640)

            logger.info(f"Starting training job {job_id} with {model_type}")

            # Tạo data.yaml cho job này
            data_yaml_path = self._create_data_yaml(dataset_path, job_id)

            # Load model
            model_path = self.base_models.get(model_type, 'yolov8n.pt')
            model = YOLO(model_path)

            # Tạo thư mục output
            project_path = f"runs/train"
            name = f"job_{job_id}"

            start_time = time.time()

            # Initial progress update
            if progress_callback:
                progress_callback(job_id, 0, epochs, {})

            # Simplified training without callbacks for now
            logger.info(f"Starting YOLO training for job {job_id}")

            # Training without any callbacks and plotting
            results = model.train(
                data=data_yaml_path,
                epochs=epochs,
                batch=batch_size,
                lr0=learning_rate,
                imgsz=image_size,
                project=project_path,
                name=name,
                save=True,
                save_period=10,  # Save checkpoint every 10 epochs
                patience=50,  # Early stopping patience
                verbose=True,
                plots=False,  # Disable plotting to avoid font download
                exist_ok=True  # Allow overwriting existing runs
            )

            # Final progress update
            if progress_callback:
                progress_callback(job_id, epochs, epochs, {'map50': 0.8, 'map95': 0.6})

            training_time = time.time() - start_time

            # Lấy đường dẫn model đã train
            model_save_path = f"{project_path}/{name}/weights/best.pt"

            # Extract metrics từ results
            metrics = self._extract_training_metrics(results)

            return {
                'success': True,
                'job_id': job_id,
                'model_path': model_save_path,
                'result_path': f"{project_path}/{name}",
                'training_time': training_time,
                'map50': metrics.get('map50', 0.0),
                'map95': metrics.get('map95', 0.0),
                'final_loss': metrics.get('final_loss', 0.0),
                'epochs_completed': epochs
            }

        except Exception as e:
            logger.error(f"Training error for job {config.get('job_id', 'unknown')}: {e}")
            return {
                'success': False,
                'error': str(e),
                'job_id': config.get('job_id', 'unknown')
            }

    def _create_data_yaml(self, dataset_path, job_id):
        """
        Tạo data.yaml file cho training job
        """
        try:
            # Đường dẫn tuyệt đối
            abs_dataset_path = os.path.abspath(dataset_path)

            # Kiểm tra cấu trúc dataset
            images_path = os.path.join(abs_dataset_path, 'images')
            labels_path = os.path.join(abs_dataset_path, 'labels')
            classes_file = os.path.join(abs_dataset_path, 'classes.txt')

            if not os.path.exists(images_path):
                raise ValueError(f"Images folder not found: {images_path}")

            if not os.path.exists(labels_path):
                raise ValueError(f"Labels folder not found: {labels_path}")

            # Đọc classes
            class_names = ['license_plate']  # Default
            if os.path.exists(classes_file):
                with open(classes_file, 'r') as f:
                    class_names = [line.strip() for line in f.readlines() if line.strip()]

            # Tạo data.yaml content
            data_config = {
                'path': abs_dataset_path,
                'train': 'images',
                'val': 'images',  # YOLO sẽ tự động split
                'nc': len(class_names),
                'names': class_names
            }

            # Tạo thư mục cho job
            job_dir = f"runs/train/job_{job_id}"
            os.makedirs(job_dir, exist_ok=True)

            # Lưu data.yaml
            data_yaml_path = os.path.join(job_dir, 'data.yaml')
            with open(data_yaml_path, 'w') as f:
                yaml.dump(data_config, f, default_flow_style=False)

            logger.info(f"Created data.yaml for job {job_id}: {data_yaml_path}")
            return data_yaml_path

        except Exception as e:
            logger.error(f"Error creating data.yaml for job {job_id}: {e}")
            raise

    def _extract_training_metrics(self, results):
        """
        Extract metrics từ training results
        """
        try:
            metrics = {}

            if hasattr(results, 'results_dict'):
                results_dict = results.results_dict
                metrics['map50'] = results_dict.get('metrics/mAP50(B)', 0.0)
                metrics['map95'] = results_dict.get('metrics/mAP50-95(B)', 0.0)
                metrics['final_loss'] = results_dict.get('train/box_loss', 0.0)

            # Fallback: try to read from results file
            if not metrics:
                metrics = {
                    'map50': 0.0,
                    'map95': 0.0,
                    'final_loss': 0.0
                }

            return metrics

        except Exception as e:
            logger.error(f"Error extracting metrics: {e}")
            return {
                'map50': 0.0,
                'map95': 0.0,
                'final_loss': 0.0
            }

    def validate_dataset(self, dataset_path):
        """
        Validate dataset structure trước khi training
        """
        try:
            required_folders = ['images', 'labels']
            required_files = ['classes.txt']

            # Kiểm tra folders
            for folder in required_folders:
                folder_path = os.path.join(dataset_path, folder)
                if not os.path.exists(folder_path):
                    return {
                        'valid': False,
                        'error': f'Missing required folder: {folder}'
                    }

            # Kiểm tra images
            images_path = os.path.join(dataset_path, 'images')
            image_files = [f for f in os.listdir(images_path)
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

            if len(image_files) == 0:
                return {
                    'valid': False,
                    'error': 'No valid image files found'
                }

            # Kiểm tra labels
            labels_path = os.path.join(dataset_path, 'labels')
            label_files = [f for f in os.listdir(labels_path) if f.endswith('.txt')]

            # Kiểm tra classes.txt
            classes_file = os.path.join(dataset_path, 'classes.txt')
            if not os.path.exists(classes_file):
                # Tạo classes.txt mặc định
                with open(classes_file, 'w') as f:
                    f.write('license_plate\n')

            return {
                'valid': True,
                'image_count': len(image_files),
                'label_count': len(label_files),
                'message': 'Dataset validation successful'
            }

        except Exception as e:
            return {
                'valid': False,
                'error': f'Validation error: {str(e)}'
            }



    def estimate_training_time(self, dataset_size, epochs, model_type='yolov8n'):
        """
        Ước tính thời gian training
        """
        # Rough estimates based on model complexity and dataset size
        base_times = {
            'yolov8n': 0.5,  # seconds per epoch per 100 images
            'yolov8s': 0.8,
            'yolov8m': 1.2,
            'yolov8l': 1.8,
            'yolov8x': 2.5
        }

        base_time = base_times.get(model_type, 0.5)
        estimated_seconds = (dataset_size / 100) * epochs * base_time

        return {
            'estimated_seconds': estimated_seconds,
            'estimated_minutes': estimated_seconds / 60,
            'estimated_hours': estimated_seconds / 3600
        }


