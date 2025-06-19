from flask import Blueprint
from controllers.training_controller import TrainingController

# Tạo Blueprint cho training routes
training_bp = Blueprint('training', __name__)

# Initialize controller
training_controller = TrainingController()

@training_bp.route('/start', methods=['POST'])
def start_training():
    """
    Bắt đầu training job mới

    JSON body:
    {
        "name": "License Plate Model v2",
        "dataset_id": 1,
        "model_type": "yolov8n",
        "epochs": 100,
        "batch_size": 16,
        "learning_rate": 0.01,
        "image_size": 640
    }
    """
    return training_controller.start_training()

@training_bp.route('/jobs', methods=['GET'])
def get_training_jobs():
    """
    Lấy danh sách tất cả training jobs
    """
    return training_controller.get_training_jobs()

@training_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_training_job(job_id):
    """
    Lấy thông tin chi tiết training job theo ID
    """
    return training_controller.get_training_job_by_id(job_id)

@training_bp.route('/jobs/<int:job_id>/status', methods=['GET'])
def get_training_status(job_id):
    """
    Kiểm tra trạng thái training job
    """
    return training_controller.get_training_job_by_id(job_id)

@training_bp.route('/jobs/<int:job_id>/stop', methods=['POST'])
def stop_training_job(job_id):
    """
    Dừng training job đang chạy
    """
    try:
        from flask import current_app
        current_app.logger.info(f"Stop route called with job_id: {job_id}, type: {type(job_id)}")
        return training_controller.stop_training_job(job_id)
    except Exception as e:
        current_app.logger.error(f"Stop route error: {e}")
        from flask import jsonify
        return jsonify({'error': f'Route error: {str(e)}'}), 500

@training_bp.route('/jobs/<int:job_id>/save-model', methods=['POST', 'OPTIONS'])
def save_model_manual(job_id):
    """Save model from training job to database"""
    from flask import request, jsonify

    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    return training_controller.save_model_from_job(job_id)

@training_bp.route('/jobs/<int:job_id>/discard-model', methods=['POST', 'OPTIONS'])
def discard_model_manual(job_id):
    """Discard model from training job and cleanup files"""
    from flask import request, jsonify

    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    return training_controller.discard_model_from_job(job_id)

@training_bp.route('/stats', methods=['GET'])
def get_training_stats():
    """
    Lấy thống kê về training jobs
    """
    return training_controller.get_training_stats()


