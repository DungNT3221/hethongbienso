import os
from flask import request, jsonify
from config.config import SessionLocal
from models.model import Model
from models.predict_log import PredictLog
from models.dataset import Dataset
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)

class ModelController:
    def get_all_models(self):
        """
        Lấy danh sách tất cả models
        """
        try:
            db = SessionLocal()
            try:
                models = db.query(Model).order_by(Model.created_at.desc()).all()

                result = []
                for model in models:
                    try:
                        model_data = {
                            'id': model.id,
                            'name': model.name,
                            'type': str(model.type),  # Force convert to string
                            'version': model.version,
                            'epochs': model.epochs,
                            'batch_size': model.batch_size,
                            'dataset_size': model.dataset_size,
                            'training_time': model.training_time,
                            'map50': model.map50,
                            'map95': model.map95,
                            'model_path': model.model_path,
                            'is_approved': getattr(model, 'is_approved', False),
                            'approval_notes': getattr(model, 'approval_notes', None),
                            'dataset_id': getattr(model, 'dataset_id', None),
                            'file_exists': os.path.exists(model.model_path) if model.model_path else False,
                            'created_at': model.created_at.isoformat() if model.created_at else None,
                            'updated_at': model.updated_at.isoformat() if model.updated_at else None
                        }
                    except Exception as e:
                        logger.error(f"Error processing model {model.id}: {e}")
                        continue

                    # Thêm thông tin dataset nếu có
                    if hasattr(model, 'dataset_id') and model.dataset_id:
                        try:
                            dataset = db.query(Dataset).filter(Dataset.id == model.dataset_id).first()
                            if dataset:
                                model_data['dataset_info'] = {
                                    'id': dataset.id,
                                    'name': dataset.name,
                                    'upload_type': str(dataset.upload_type),
                                    'labeling_method': str(dataset.labeling_method)
                                }
                        except Exception as e:
                            logger.error(f"Error getting dataset info for model {model.id}: {e}")

                    result.append(model_data)

                return jsonify({
                    'success': True,
                    'models': result,
                    'total': len(result)
                }), 200

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Get all models error: {e}")
            return jsonify({'error': str(e)}), 500

    def get_model_by_id(self, model_id):
        """
        Lấy thông tin chi tiết model theo ID
        """
        try:
            db = SessionLocal()
            try:
                model = db.query(Model).filter(Model.id == model_id).first()

                if not model:
                    return jsonify({'error': 'Model not found'}), 404

                # Đếm số lần predict
                predict_count = db.query(func.count(PredictLog.id)).filter(
                    PredictLog.model_id == model_id
                ).scalar() or 0

                result = {
                    'id': model.id,
                    'name': model.name,
                    'type': model.type,
                    'version': model.version,
                    'epochs': model.epochs,
                    'batch_size': model.batch_size,
                    'dataset_size': model.dataset_size,
                    'training_time': model.training_time,
                    'map50': model.map50,
                    'map95': model.map95,
                    'model_path': model.model_path,
                    'is_approved': getattr(model, 'is_approved', False),
                    'approval_notes': getattr(model, 'approval_notes', None),
                    'dataset_id': getattr(model, 'dataset_id', None),
                    'file_exists': os.path.exists(model.model_path) if model.model_path else False,
                    'predict_count': predict_count,
                    'created_at': model.created_at.isoformat() if model.created_at else None,
                    'updated_at': model.updated_at.isoformat() if model.updated_at else None
                }

                # Thêm thông tin dataset
                if hasattr(model, 'dataset_id') and model.dataset_id:
                    dataset = db.query(Dataset).filter(Dataset.id == model.dataset_id).first()
                    if dataset:
                        result['dataset_info'] = {
                            'id': dataset.id,
                            'name': dataset.name,
                            'upload_type': str(dataset.upload_type),
                            'labeling_method': str(dataset.labeling_method),
                            'status': str(dataset.status)
                        }

                return jsonify({
                    'success': True,
                    'model': result
                }), 200

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Get model by ID error: {e}")
            return jsonify({'error': str(e)}), 500

    def approve_model(self, model_id):
        """
        Approve model để có thể sử dụng cho prediction
        """
        try:
            approval_notes = request.json.get('notes', '')

            db = SessionLocal()
            try:
                model = db.query(Model).filter(Model.id == model_id).first()

                if not model:
                    return jsonify({'error': 'Model not found'}), 404

                # Update approval status
                if hasattr(model, 'is_approved'):
                    model.is_approved = True
                if hasattr(model, 'approval_notes'):
                    model.approval_notes = approval_notes

                db.commit()

                return jsonify({
                    'success': True,
                    'message': 'Model approved successfully',
                    'model_id': model_id
                }), 200

            except Exception as e:
                db.rollback()
                logger.error(f"Approve model error: {e}")
                return jsonify({'error': 'Failed to approve model'}), 500
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Approve model error: {e}")
            return jsonify({'error': str(e)}), 500

    def reject_model(self, model_id):
        """
        Reject model với lý do
        """
        try:
            rejection_reason = request.json.get('reason', 'No reason provided')

            db = SessionLocal()
            try:
                model = db.query(Model).filter(Model.id == model_id).first()

                if not model:
                    return jsonify({'error': 'Model not found'}), 404

                # Update approval status
                if hasattr(model, 'is_approved'):
                    model.is_approved = False
                if hasattr(model, 'approval_notes'):
                    model.approval_notes = f"REJECTED: {rejection_reason}"

                db.commit()

                return jsonify({
                    'success': True,
                    'message': 'Model rejected',
                    'model_id': model_id,
                    'reason': rejection_reason
                }), 200

            except Exception as e:
                db.rollback()
                logger.error(f"Reject model error: {e}")
                return jsonify({'error': 'Failed to reject model'}), 500
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Reject model error: {e}")
            return jsonify({'error': str(e)}), 500

    def delete_model(self, model_id):
        """
        Xóa model
        """
        try:
            db = SessionLocal()
            try:
                model = db.query(Model).filter(Model.id == model_id).first()

                if not model:
                    return jsonify({'error': 'Model not found'}), 404

                # Xóa file model nếu tồn tại
                if model.model_path and os.path.exists(model.model_path):
                    try:
                        os.remove(model.model_path)
                    except Exception as e:
                        logger.warning(f"Could not delete model file {model.model_path}: {e}")

                # Xóa record
                db.delete(model)
                db.commit()

                return jsonify({
                    'success': True,
                    'message': 'Model deleted successfully'
                }), 200

            except Exception as e:
                db.rollback()
                logger.error(f"Delete model error: {e}")
                return jsonify({'error': 'Failed to delete model'}), 500
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Delete model error: {e}")
            return jsonify({'error': str(e)}), 500

    def get_approved_models(self):
        """
        Lấy danh sách models đã được approve (để dùng cho prediction)
        """
        try:
            db = SessionLocal()
            try:
                # Query models đã approved
                models = db.query(Model).filter(
                    getattr(Model, 'is_approved', True) == True
                ).order_by(Model.created_at.desc()).all()

                result = []
                for model in models:
                    model_data = {
                        'id': model.id,
                        'name': model.name,
                        'type': model.type,
                        'version': model.version,
                        'map50': model.map50,
                        'map95': model.map95,
                        'model_path': model.model_path,
                        'file_exists': os.path.exists(model.model_path) if model.model_path else False,
                        'created_at': model.created_at.isoformat() if model.created_at else None
                    }
                    result.append(model_data)

                return jsonify({
                    'success': True,
                    'approved_models': result,
                    'total': len(result)
                }), 200

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Get approved models error: {e}")
            return jsonify({'error': str(e)}), 500

    def get_model_stats(self):
        """
        Lấy thống kê về models
        """
        try:
            db = SessionLocal()
            try:
                # Tổng số models
                total_models = db.query(func.count(Model.id)).scalar() or 0

                # Số models đã approved
                approved_models = db.query(func.count(Model.id)).filter(
                    getattr(Model, 'is_approved', True) == True
                ).scalar() or 0

                # Tổng số predictions
                total_predictions = db.query(func.count(PredictLog.id)).scalar() or 0

                # Model được sử dụng nhiều nhất
                most_used_model = db.query(
                    Model.id, Model.name, func.count(PredictLog.id).label('usage_count')
                ).join(PredictLog, Model.id == PredictLog.model_id, isouter=True).group_by(
                    Model.id, Model.name
                ).order_by(func.count(PredictLog.id).desc()).first()

                # Thời gian training trung bình
                avg_training_time = db.query(func.avg(Model.training_time)).scalar()

                result = {
                    'total_models': total_models,
                    'approved_models': approved_models,
                    'pending_approval': total_models - approved_models,
                    'total_predictions': total_predictions,
                    'most_used_model': {
                        'id': most_used_model[0],
                        'name': most_used_model[1],
                        'usage_count': most_used_model[2]
                    } if most_used_model else None,
                    'avg_training_time': float(avg_training_time) if avg_training_time else 0
                }

                return jsonify({
                    'success': True,
                    'stats': result
                }), 200

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Get model stats error: {e}")
            return jsonify({'error': str(e)}), 500
