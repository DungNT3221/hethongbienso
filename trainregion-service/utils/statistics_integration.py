import requests
import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class StatisticsIntegration:
    """
    Integration utility để gửi training data đến model-statistics-service
    """
    
    def __init__(self):
        self.statistics_service_url = os.getenv('MODELSTATS_SERVICE_URL', 'http://model-statistics-service:3004')
        self.timeout = 10  # seconds
        
    def send_training_record(self, training_data: Dict[str, Any]) -> bool:
        """
        Gửi training record đến model-statistics-service
        
        Args:
            training_data: Dictionary chứa training data
            
        Returns:
            bool: True nếu thành công, False nếu thất bại
        """
        try:
            url = f"{self.statistics_service_url}/api/statistics/training"
            
            response = requests.post(
                url,
                json=training_data,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                logger.info(f"Successfully sent training record to statistics service")
                return True
            else:
                logger.error(f"Failed to send training record: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending training record to statistics service: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending training record: {e}")
            return False
    
    def send_training_completed(self, job_id: int, job_data: Dict[str, Any], 
                              dataset_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Gửi thông tin training completed đến statistics service
        
        Args:
            job_id: ID của training job
            job_data: Data từ training job
            dataset_data: Data từ dataset (optional)
            
        Returns:
            bool: True nếu thành công
        """
        try:
            training_record = {
                'model_id': None,  # Chưa có model_id vì chưa save
                'model_name': job_data.get('name', f'Training Job {job_id}'),
                'model_type': job_data.get('model_type', 'yolov8n'),
                'dataset_name': dataset_data.get('name') if dataset_data else None,
                'dataset_size': dataset_data.get('image_count', 0) if dataset_data else 0,
                'epochs': job_data.get('epochs', 0),
                'batch_size': job_data.get('batch_size', 0),
                'learning_rate': job_data.get('learning_rate', 0.0),
                'training_time': job_data.get('training_time', 0.0),
                'map50': job_data.get('best_map50', 0.0),
                'map95': job_data.get('best_map95', 0.0),
                'status': 'completed',
                'is_approved': False,
                'model_path': job_data.get('model_path', '')
            }
            
            return self.send_training_record(training_record)
            
        except Exception as e:
            logger.error(f"Error preparing training completed data: {e}")
            return False
    
    def send_model_saved(self, job_id: int, model_id: int, model_name: str, 
                        job_data: Dict[str, Any], dataset_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Gửi thông tin model đã được save đến statistics service
        
        Args:
            job_id: ID của training job
            model_id: ID của model đã save
            model_name: Tên model
            job_data: Data từ training job
            dataset_data: Data từ dataset (optional)
            
        Returns:
            bool: True nếu thành công
        """
        try:
            training_record = {
                'model_id': model_id,
                'model_name': model_name,
                'model_type': job_data.get('model_type', 'yolov8n'),
                'dataset_name': dataset_data.get('name') if dataset_data else None,
                'dataset_size': dataset_data.get('image_count', 0) if dataset_data else 0,
                'epochs': job_data.get('epochs', 0),
                'batch_size': job_data.get('batch_size', 0),
                'learning_rate': job_data.get('learning_rate', 0.0),
                'training_time': job_data.get('training_time', 0.0),
                'map50': job_data.get('best_map50', 0.0),
                'map95': job_data.get('best_map95', 0.0),
                'status': 'completed',
                'is_approved': True,  # Model đã được save = approved
                'model_path': job_data.get('model_path', '')
            }
            
            return self.send_training_record(training_record)
            
        except Exception as e:
            logger.error(f"Error preparing model saved data: {e}")
            return False
    
    def send_training_failed(self, job_id: int, job_data: Dict[str, Any], 
                           error_message: str, dataset_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Gửi thông tin training failed đến statistics service
        
        Args:
            job_id: ID của training job
            job_data: Data từ training job
            error_message: Lỗi message
            dataset_data: Data từ dataset (optional)
            
        Returns:
            bool: True nếu thành công
        """
        try:
            training_record = {
                'model_id': None,
                'model_name': job_data.get('name', f'Failed Training Job {job_id}'),
                'model_type': job_data.get('model_type', 'yolov8n'),
                'dataset_name': dataset_data.get('name') if dataset_data else None,
                'dataset_size': dataset_data.get('image_count', 0) if dataset_data else 0,
                'epochs': job_data.get('epochs', 0),
                'batch_size': job_data.get('batch_size', 0),
                'learning_rate': job_data.get('learning_rate', 0.0),
                'training_time': job_data.get('training_time', 0.0),
                'map50': 0.0,  # Failed training has no metrics
                'map95': 0.0,
                'status': 'failed',
                'is_approved': False,
                'model_path': ''
            }
            
            return self.send_training_record(training_record)
            
        except Exception as e:
            logger.error(f"Error preparing training failed data: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Test connection đến model-statistics-service
        
        Returns:
            bool: True nếu service available
        """
        try:
            url = f"{self.statistics_service_url}/health"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                logger.info("Statistics service connection test successful")
                return True
            else:
                logger.warning(f"Statistics service returned {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"Statistics service not available: {e}")
            return False
        except Exception as e:
            logger.error(f"Error testing statistics service connection: {e}")
            return False

# Global instance
statistics_integration = StatisticsIntegration()
