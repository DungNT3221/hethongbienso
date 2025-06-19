from flask import Blueprint
from controllers.dataset_controller import DatasetController

# Tạo Blueprint cho dataset routes
dataset_bp = Blueprint('dataset', __name__)

# Initialize controller
dataset_controller = DatasetController()

@dataset_bp.route('/upload-images', methods=['POST'])
def upload_images():
    """
    Upload nhiều ảnh với auto-labeling
    
    Form data:
    - images: List of image files
    - method: 'auto', 'template', or 'manual' (default: 'auto')
    - name: Dataset name
    - description: Dataset description (optional)
    - confidence_threshold: Confidence threshold for auto-labeling (default: 0.3)
    """
    return dataset_controller.upload_images_smart()

@dataset_bp.route('/upload-zip', methods=['POST'])
def upload_zip():
    """
    Upload ZIP file chứa dataset hoàn chỉnh
    
    Form data:
    - dataset: ZIP file
    - name: Dataset name
    - description: Dataset description (optional)
    """
    return dataset_controller.upload_zip_dataset()

@dataset_bp.route('/', methods=['GET'], strict_slashes=False)
def get_datasets():
    """
    Lấy danh sách tất cả datasets
    """
    return dataset_controller.get_all_datasets()

@dataset_bp.route('/<int:dataset_id>', methods=['GET'])
def get_dataset(dataset_id):
    """
    Lấy thông tin chi tiết dataset theo ID
    """
    return dataset_controller.get_dataset_by_id(dataset_id)

@dataset_bp.route('/<int:dataset_id>', methods=['DELETE'])
def delete_dataset(dataset_id):
    """
    Xóa dataset
    """
    return dataset_controller.delete_dataset(dataset_id)

@dataset_bp.route('/<int:dataset_id>/preview', methods=['GET'])
def get_dataset_preview(dataset_id):
    """
    Lấy preview dataset với images và annotations
    """
    return dataset_controller.get_dataset_preview(dataset_id)

@dataset_bp.route('/auto-labeler/info', methods=['GET'])
def get_auto_labeler_info():
    """
    Lấy thông tin về auto-labeler hiện tại
    """
    return dataset_controller.get_auto_labeler_info()
