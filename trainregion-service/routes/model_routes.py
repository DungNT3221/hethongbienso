from flask import Blueprint
from controllers.model_controller import ModelController

# Tạo Blueprint cho model routes
model_bp = Blueprint('model', __name__)

# Initialize controller
model_controller = ModelController()

@model_bp.route('/', methods=['GET'])
def get_models():
    """
    Lấy danh sách tất cả models
    """
    return model_controller.get_all_models()

@model_bp.route('/<int:model_id>', methods=['GET'])
def get_model(model_id):
    """
    Lấy thông tin chi tiết model theo ID
    """
    return model_controller.get_model_by_id(model_id)

@model_bp.route('/<int:model_id>/approve', methods=['POST'])
def approve_model(model_id):
    """
    Approve model để có thể sử dụng cho prediction
    
    JSON body:
    {
        "notes": "Model approved for production use"
    }
    """
    return model_controller.approve_model(model_id)

@model_bp.route('/<int:model_id>/reject', methods=['POST'])
def reject_model(model_id):
    """
    Reject model với lý do
    
    JSON body:
    {
        "reason": "Low accuracy, needs more training data"
    }
    """
    return model_controller.reject_model(model_id)

@model_bp.route('/<int:model_id>', methods=['DELETE'])
def delete_model(model_id):
    """
    Xóa model
    """
    return model_controller.delete_model(model_id)

@model_bp.route('/approved', methods=['GET'])
def get_approved_models():
    """
    Lấy danh sách models đã được approve (để dùng cho prediction)
    """
    return model_controller.get_approved_models()

@model_bp.route('/stats', methods=['GET'])
def get_model_stats():
    """
    Lấy thống kê về models
    """
    return model_controller.get_model_stats()
