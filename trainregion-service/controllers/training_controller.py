import os
import threading
import time
from flask import request, jsonify
from config.config import SessionLocal
from models.training_job import TrainingJob
from models.model import Model
from models.dataset import Dataset
from utils.training_utils import TrainingUtils
from utils.statistics_integration import statistics_integration
import logging

logger = logging.getLogger(__name__)

class TrainingController:
    def __init__(self):
        self.training_utils = TrainingUtils()
        self.active_jobs = {}  # Track active training jobs

    def start_training(self):
        """
        Bắt đầu training job mới với dataset đã upload
        """
        try:
            data = request.get_json()

            # Validate required fields
            required_fields = ['name', 'dataset_id', 'model_type']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400

            dataset_id = data['dataset_id']

            db = SessionLocal()
            try:
                # Kiểm tra dataset tồn tại
                dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
                if not dataset:
                    return jsonify({'error': 'Dataset not found'}), 404

                if dataset.status != 'ready':
                    return jsonify({'error': 'Dataset is not ready for training'}), 400

                # Tạo training job record
                training_job = TrainingJob(
                    name=data['name'],
                    dataset_id=dataset_id,
                    model_type=data.get('model_type', 'yolov8n'),
                    epochs=data.get('epochs', 100),
                    batch_size=data.get('batch_size', 16),
                    learning_rate=data.get('learning_rate', 0.01),
                    image_size=data.get('image_size', 640),
                    status='pending',
                    progress=0.0
                )

                db.add(training_job)
                db.commit()
                db.refresh(training_job)

                # Bắt đầu training trong background thread
                training_thread = threading.Thread(
                    target=self._run_training_job,
                    args=(training_job.id, dataset.upload_path)
                )
                training_thread.daemon = True
                training_thread.start()

                # Track active job
                self.active_jobs[training_job.id] = {
                    'thread': training_thread,
                    'start_time': time.time(),
                    'status': 'running',
                    'stop_requested': False
                }

                return jsonify({
                    'success': True,
                    'training_job': {
                        'id': training_job.id,
                        'name': training_job.name,
                        'status': training_job.status,
                        'dataset_id': dataset_id,
                        'model_type': training_job.model_type,
                        'epochs': training_job.epochs,
                        'batch_size': training_job.batch_size
                    }
                }), 201

            except Exception as e:
                db.rollback()
                logger.error(f"Database error: {e}")
                return jsonify({'error': 'Database error occurred'}), 500
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Start training error: {e}")
            return jsonify({'error': str(e)}), 500

    def get_training_jobs(self):
        """
        Lấy danh sách tất cả training jobs
        """
        try:
            db = SessionLocal()
            try:
                jobs = db.query(TrainingJob).order_by(TrainingJob.created_at.desc()).all()

                result = []
                for job in jobs:
                    job_data = {
                        'id': job.id,
                        'name': getattr(job, 'name', f'Job {job.id}'),
                        'dataset_id': getattr(job, 'dataset_id', None),
                        'model_type': getattr(job, 'model_type', 'yolov8n'),
                        'epochs': getattr(job, 'epochs', 100),
                        'batch_size': getattr(job, 'batch_size', 16),
                        'learning_rate': getattr(job, 'learning_rate', 0.01),
                        'image_size': getattr(job, 'image_size', 640),
                        'status': job.status,
                        'progress': getattr(job, 'progress', 0.0),
                        'current_epoch': getattr(job, 'current_epoch', 0),
                        'best_map50': getattr(job, 'best_map50', 0.0),
                        'best_map95': getattr(job, 'best_map95', 0.0),
                        'training_time': getattr(job, 'training_time', 0.0),
                        'result_path': getattr(job, 'result_path', None),
                        'created_at': job.created_at.isoformat(),
                        'updated_at': job.updated_at.isoformat()
                    }

                    # Thêm thông tin dataset
                    if job_data['dataset_id']:
                        dataset = db.query(Dataset).filter(Dataset.id == job_data['dataset_id']).first()
                        if dataset:
                            job_data['dataset_info'] = {
                                'name': dataset.name,
                                'upload_type': dataset.upload_type,
                                'image_count': dataset.image_count
                            }

                    result.append(job_data)

                return jsonify({
                    'success': True,
                    'training_jobs': result,
                    'total': len(result)
                }), 200

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Get training jobs error: {e}")
            return jsonify({'error': str(e)}), 500

    def get_training_job_by_id(self, job_id):
        """
        Lấy thông tin chi tiết training job
        """
        try:
            db = SessionLocal()
            try:
                job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()

                if not job:
                    return jsonify({'error': 'Training job not found'}), 404

                result = {
                    'id': job.id,
                    'name': getattr(job, 'name', f'Job {job.id}'),
                    'dataset_id': getattr(job, 'dataset_id', None),
                    'model_type': getattr(job, 'model_type', 'yolov8n'),
                    'epochs': getattr(job, 'epochs', 100),
                    'batch_size': getattr(job, 'batch_size', 16),
                    'learning_rate': getattr(job, 'learning_rate', 0.01),
                    'image_size': getattr(job, 'image_size', 640),
                    'status': job.status,
                    'progress': getattr(job, 'progress', 0.0),
                    'current_epoch': getattr(job, 'current_epoch', 0),
                    'best_map50': getattr(job, 'best_map50', 0.0),
                    'best_map95': getattr(job, 'best_map95', 0.0),
                    'training_time': getattr(job, 'training_time', 0.0),
                    'result_path': getattr(job, 'result_path', None),
                    'created_at': job.created_at.isoformat(),
                    'updated_at': job.updated_at.isoformat()
                }

                # Thêm thông tin dataset
                if result['dataset_id']:
                    dataset = db.query(Dataset).filter(Dataset.id == result['dataset_id']).first()
                    if dataset:
                        result['dataset_info'] = dataset.to_dict()

                # Thêm thông tin active job
                if job_id in self.active_jobs:
                    result['is_active'] = True
                    result['runtime'] = time.time() - self.active_jobs[job_id]['start_time']
                else:
                    result['is_active'] = False

                return jsonify({
                    'success': True,
                    'training_job': result
                }), 200

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Get training job error: {e}")
            return jsonify({'error': str(e)}), 500

    def stop_training_job(self, job_id):
        """
        Dừng training job đang chạy
        """
        try:
            # Ensure job_id is integer
            try:
                job_id = int(job_id)
            except (ValueError, TypeError):
                logger.error(f"Invalid job_id: {job_id}")
                return jsonify({'error': 'Invalid job ID'}), 400

            logger.info(f"Attempting to stop training job {job_id}")
            logger.info(f"Current active jobs: {list(self.active_jobs.keys())}")

            # Update status in database first
            db = SessionLocal()
            try:
                job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
                if not job:
                    logger.error(f"Training job {job_id} not found in database")
                    return jsonify({'error': 'Training job not found'}), 404

                logger.info(f"Job {job_id} current status: {job.status}")

                # Handle different job statuses
                if job.status == 'stopped':
                    return jsonify({
                        'success': True,
                        'message': f'Job {job_id} is already stopped'
                    }), 200
                elif job.status in ['completed', 'failed']:
                    # Force update to stopped for cleanup
                    job.status = 'stopped'
                    db.commit()
                    logger.info(f"Job {job_id} status changed from {job.status} to 'stopped'")

                    # Clean up active jobs if exists
                    if job_id in self.active_jobs:
                        del self.active_jobs[job_id]
                        logger.info(f"Cleaned up active job {job_id}")

                    return jsonify({
                        'success': True,
                        'message': f'Job {job_id} was {job.status}, now marked as stopped'
                    }), 200
                elif job.status in ['running', 'pending']:
                    # Normal stop process
                    job.status = 'stopped'
                    db.commit()
                    logger.info(f"Job {job_id} status updated to 'stopped' in database")

                    # Set stop flag for the training process
                    if job_id in self.active_jobs:
                        self.active_jobs[job_id]['status'] = 'stopped'
                        self.active_jobs[job_id]['stop_requested'] = True
                        logger.info(f"Stop flag set for job {job_id}")

                    return jsonify({
                        'success': True,
                        'message': f'Stop signal sent to training job {job_id}. Training will stop after current epoch.'
                    }), 200
                else:
                    # Unknown status
                    job.status = 'stopped'
                    db.commit()
                    return jsonify({
                        'success': True,
                        'message': f'Job {job_id} status was {job.status}, now stopped'
                    }), 200

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Stop training job error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    def _run_training_job(self, job_id, dataset_path):
        """
        Chạy training job trong background thread
        """
        db = SessionLocal()
        try:
            job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
            if not job:
                logger.error(f"Training job {job_id} not found")
                return

            # Update status to running
            job.status = 'running'
            db.commit()

            # Prepare training config
            config = {
                'job_id': job_id,
                'dataset_path': dataset_path,
                'model_type': getattr(job, 'model_type', 'yolov8n'),
                'epochs': getattr(job, 'epochs', 100),
                'batch_size': getattr(job, 'batch_size', 16),
                'learning_rate': getattr(job, 'learning_rate', 0.01),
                'image_size': getattr(job, 'image_size', 640)
            }

            # Run training with stop check callback
            def check_stop_callback():
                if job_id in self.active_jobs:
                    return self.active_jobs[job_id].get('stop_requested', False)
                return False

            result = self.training_utils.run_training(config, self._update_progress_callback, check_stop_callback)

            if result['success']:
                # Training completed successfully
                job.status = 'completed'
                job.progress = 100.0
                job.best_map50 = result.get('map50', 0.0)
                job.best_map95 = result.get('map95', 0.0)
                job.training_time = result.get('training_time', 0.0)
                job.result_path = result.get('result_path', '')

                # Store model path for later manual save
                job.model_path = result.get('model_path', '')
                job.model_saved = False  # Not saved to models table yet

                logger.info(f"Training job {job_id} completed successfully - waiting for manual save")

            else:
                # Training failed
                job.status = 'failed'
                logger.error(f"Training job {job_id} failed: {result.get('error', 'Unknown error')}")

            db.commit()

        except Exception as e:
            logger.error(f"Training job {job_id} error: {e}")
            job.status = 'failed'
            db.commit()
        finally:
            db.close()
            # Remove from active jobs
            if job_id in self.active_jobs:
                logger.info(f"Removing job {job_id} from active jobs")
                del self.active_jobs[job_id]

    def _update_progress_callback(self, job_id, epoch, total_epochs, metrics):
        """
        Callback để update progress trong database
        """
        try:
            logger.info(f"Updating progress for job {job_id}: epoch {epoch}/{total_epochs}")

            db = SessionLocal()
            try:
                job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
                if job:
                    progress = (epoch / total_epochs) * 100
                    job.progress = progress
                    job.current_epoch = epoch

                    logger.info(f"Job {job_id} progress updated: {progress:.1f}%")

                    if 'map50' in metrics:
                        old_map50 = getattr(job, 'best_map50', 0.0) or 0.0
                        job.best_map50 = max(old_map50, metrics['map50'])
                        logger.info(f"Job {job_id} mAP50: {job.best_map50:.3f}")

                    if 'map95' in metrics:
                        old_map95 = getattr(job, 'best_map95', 0.0) or 0.0
                        job.best_map95 = max(old_map95, metrics['map95'])
                        logger.info(f"Job {job_id} mAP95: {job.best_map95:.3f}")

                    db.commit()
                    logger.info(f"Job {job_id} progress committed to database")
                else:
                    logger.error(f"Job {job_id} not found in database")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Update progress error for job {job_id}: {e}")
            import traceback
            logger.error(traceback.format_exc())



    def get_training_stats(self):
        """
        Lấy thống kê về training jobs
        """
        try:
            db = SessionLocal()
            try:
                # Tổng số jobs
                total_jobs = db.query(TrainingJob).count()

                # Jobs theo status
                completed_jobs = db.query(TrainingJob).filter(TrainingJob.status == 'completed').count()
                running_jobs = db.query(TrainingJob).filter(TrainingJob.status == 'running').count()
                failed_jobs = db.query(TrainingJob).filter(TrainingJob.status == 'failed').count()

                # Active jobs
                active_jobs_count = len(self.active_jobs)

                result = {
                    'total_jobs': total_jobs,
                    'completed_jobs': completed_jobs,
                    'running_jobs': running_jobs,
                    'failed_jobs': failed_jobs,
                    'active_jobs': active_jobs_count,
                    'success_rate': (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0
                }

                return jsonify({
                    'success': True,
                    'stats': result
                }), 200

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Get training stats error: {e}")
            return jsonify({'error': str(e)}), 500

    def save_model_from_job(self, job_id):
        """
        Lưu model từ training job vào database sau khi user approve
        """
        try:
            from flask import request, jsonify
            import shutil
            import os
            from models.model import Model

            data = request.get_json()
            model_name = data.get('model_name', '').strip()
            notes = data.get('notes', '').strip()

            if not model_name:
                return jsonify({'error': 'Model name is required'}), 400

            db = SessionLocal()
            try:
                # Get training job
                job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
                if not job:
                    return jsonify({'error': 'Training job not found'}), 404

                if job.status != 'completed':
                    return jsonify({'error': 'Training job is not completed'}), 400

                if getattr(job, 'model_saved', False):
                    return jsonify({'error': 'Model already saved'}), 400

                # Check if model file exists
                temp_model_path = getattr(job, 'model_path', '')
                if not temp_model_path or not os.path.exists(temp_model_path):
                    return jsonify({'error': 'Model file not found'}), 404

                # Create permanent model directory
                permanent_dir = f"models/job_{job_id}"
                os.makedirs(permanent_dir, exist_ok=True)

                # Copy model to permanent location
                permanent_model_path = f"{permanent_dir}/best.pt"
                shutil.copy2(temp_model_path, permanent_model_path)

                # Create model record
                model = Model(
                    name=model_name,
                    type=getattr(job, 'model_type', 'yolov8n'),
                    version='1.0',
                    epochs=getattr(job, 'epochs', 100),
                    batch_size=getattr(job, 'batch_size', 16),
                    dataset_size=0,  # Will be updated if needed
                    training_time=getattr(job, 'training_time', 0.0),
                    map50=getattr(job, 'best_map50', 0.0),
                    map95=getattr(job, 'best_map95', 0.0),
                    model_path=permanent_model_path,
                    dataset_id=getattr(job, 'dataset_id', None),
                    approval_notes=notes,  # Fixed: use approval_notes instead of notes
                    is_approved=False  # Cần approval sau
                )

                db.add(model)

                # Mark job as model saved
                job.model_saved = True

                db.commit()

                # Send data to model-statistics-service
                try:
                    dataset = db.query(Dataset).filter(Dataset.id == job.dataset_id).first() if job.dataset_id else None

                    job_data = {
                        'name': job.name,
                        'model_type': job.model_type,
                        'epochs': job.epochs,
                        'batch_size': job.batch_size,
                        'learning_rate': job.learning_rate,
                        'training_time': getattr(job, 'training_time', 0.0),
                        'best_map50': getattr(job, 'best_map50', 0.0),
                        'best_map95': getattr(job, 'best_map95', 0.0),
                        'model_path': getattr(job, 'model_path', '')
                    }

                    dataset_data = {
                        'name': dataset.name,
                        'image_count': dataset.image_count
                    } if dataset else None

                    statistics_integration.send_model_saved(
                        job_id=job_id,
                        model_id=model.id,
                        model_name=model_name,
                        job_data=job_data,
                        dataset_data=dataset_data
                    )

                except Exception as e:
                    logger.warning(f"Failed to send model saved data to statistics service: {e}")

                logger.info(f"Model saved successfully for job {job_id}: {model_name}")

                return jsonify({
                    'success': True,
                    'message': 'Model saved to database successfully',
                    'model_id': model.id,
                    'model_name': model_name
                }), 201

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Save model error: {e}")
            return jsonify({'error': str(e)}), 500

    def discard_model_from_job(self, job_id):
        """
        Xóa model file khi user từ chối save
        """
        try:
            import os
            import shutil

            db = SessionLocal()
            try:
                # Get training job
                job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
                if not job:
                    return jsonify({'error': 'Training job not found'}), 404

                # Get model path
                temp_model_path = getattr(job, 'model_path', '')
                result_path = getattr(job, 'result_path', '')

                # Delete model file
                if temp_model_path and os.path.exists(temp_model_path):
                    try:
                        os.remove(temp_model_path)
                        logger.info(f"Deleted model file: {temp_model_path}")
                    except Exception as e:
                        logger.warning(f"Could not delete model file {temp_model_path}: {e}")

                # Delete entire result directory
                if result_path and os.path.exists(result_path):
                    try:
                        shutil.rmtree(result_path)
                        logger.info(f"Deleted result directory: {result_path}")
                    except Exception as e:
                        logger.warning(f"Could not delete result directory {result_path}: {e}")

                # Send training completed data to model-statistics-service (before deleting job)
                try:
                    dataset = db.query(Dataset).filter(Dataset.id == job.dataset_id).first() if job.dataset_id else None

                    job_data = {
                        'name': job.name,
                        'model_type': job.model_type,
                        'epochs': job.epochs,
                        'batch_size': job.batch_size,
                        'learning_rate': job.learning_rate,
                        'training_time': getattr(job, 'training_time', 0.0),
                        'best_map50': getattr(job, 'best_map50', 0.0),
                        'best_map95': getattr(job, 'best_map95', 0.0),
                        'model_path': getattr(job, 'model_path', '')
                    }

                    dataset_data = {
                        'name': dataset.name,
                        'image_count': dataset.image_count
                    } if dataset else None

                    statistics_integration.send_training_completed(
                        job_id=job_id,
                        job_data=job_data,
                        dataset_data=dataset_data
                    )

                except Exception as e:
                    logger.warning(f"Failed to send training completed data to statistics service: {e}")

                # DELETE training job record (as per statistics approach)
                db.delete(job)
                db.commit()

                logger.info(f"Model discarded and job {job_id} deleted - statistics preserved")

                return jsonify({
                    'success': True,
                    'message': 'Model discarded successfully'
                }), 200

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Discard model error: {e}")
            return jsonify({'error': str(e)}), 500




