import os
import zipfile
from flask import request, jsonify
from config.config import SessionLocal
from models.dataset import Dataset
from utils.auto_labeling import AutoLabeler
import logging
import glob

logger = logging.getLogger(__name__)

class DatasetController:
    def __init__(self):
        self.auto_labeler = AutoLabeler()
        self.upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def upload_images_smart(self):
        """
        Upload nhiều ảnh với auto-labeling
        """
        try:
            files = request.files.getlist('images')
            method = request.form.get('method', 'auto')
            dataset_name = request.form.get('name', 'Untitled Dataset')
            description = request.form.get('description', '')
            confidence_threshold = float(request.form.get('confidence_threshold', 0.3))
            
            if not files:
                return jsonify({'error': 'No images provided'}), 400
            
            # Validate image files
            valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
            valid_files = []
            total_size = 0
            
            for file in files:
                if file.filename:
                    ext = os.path.splitext(file.filename.lower())[1]
                    if ext in valid_extensions:
                        valid_files.append(file)
                        # Estimate file size (rough)
                        file.seek(0, 2)  # Seek to end
                        total_size += file.tell()
                        file.seek(0)  # Reset to beginning
            
            if not valid_files:
                return jsonify({'error': 'No valid image files found'}), 400
            
            db = SessionLocal()
            try:
                # Tạo dataset record
                dataset = Dataset(
                    name=dataset_name,
                    description=description,
                    upload_path='',  # Sẽ update sau
                    image_count=len(valid_files),
                    file_size=total_size,
                    upload_type='images',
                    has_labels=False,  # Sẽ update sau
                    labeling_method=method,
                    status='processing'
                )
                
                db.add(dataset)
                db.commit()
                db.refresh(dataset)
                
                # Update upload path
                dataset.upload_path = f"uploads/dataset_{dataset.id}"
                
                # Tạo thư mục uploads nếu chưa có
                os.makedirs("uploads", exist_ok=True)
                
                # Process images với auto-labeling
                result = self.auto_labeler.process_images(
                    valid_files, 
                    dataset.id, 
                    method, 
                    confidence_threshold
                )
                
                # Update dataset với kết quả
                dataset.has_labels = result['labeled_images'] > 0
                dataset.labeling_accuracy = result['accuracy_estimate']
                dataset.status = 'ready'
                
                db.commit()
                
                return jsonify({
                    'success': True,
                    'dataset': dataset.to_dict(),
                    'labeling_result': result
                }), 201
                
            except Exception as e:
                db.rollback()
                logger.error(f"Database error: {e}")
                return jsonify({'error': 'Database error occurred'}), 500
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return jsonify({'error': str(e)}), 500
    
    def upload_zip_dataset(self):
        """
        Upload ZIP file chứa dataset hoàn chỉnh
        """
        try:
            if 'dataset' not in request.files:
                return jsonify({'error': 'No dataset file provided'}), 400
            
            file = request.files['dataset']
            dataset_name = request.form.get('name', 'Untitled Dataset')
            description = request.form.get('description', '')
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not file.filename.lower().endswith('.zip'):
                return jsonify({'error': 'File must be a ZIP archive'}), 400
            
            db = SessionLocal()
            try:
                # Tạo dataset record
                dataset = Dataset(
                    name=dataset_name,
                    description=description,
                    upload_path='',
                    upload_type='zip',
                    has_labels=False,
                    labeling_method='manual',
                    status='processing'
                )
                
                db.add(dataset)
                db.commit()
                db.refresh(dataset)
                
                # Lưu và extract ZIP file
                dataset_path = f"uploads/dataset_{dataset.id}"
                zip_path = f"{dataset_path}.zip"
                
                os.makedirs("uploads", exist_ok=True)
                file.save(zip_path)
                
                # Extract và validate
                validation_result = self._extract_and_validate_zip(zip_path, dataset_path)
                
                if not validation_result['valid']:
                    dataset.status = 'error'
                    db.commit()
                    return jsonify({'error': validation_result['message']}), 400
                
                # Update dataset
                dataset.upload_path = dataset_path
                dataset.image_count = validation_result['image_count']
                dataset.file_size = os.path.getsize(zip_path)
                dataset.has_labels = validation_result['has_labels']
                dataset.status = 'ready'
                
                db.commit()
                
                # Xóa ZIP file sau khi extract
                os.remove(zip_path)
                
                return jsonify({
                    'success': True,
                    'dataset': dataset.to_dict(),
                    'validation_result': validation_result
                }), 201
                
            except Exception as e:
                db.rollback()
                logger.error(f"Database error: {e}")
                return jsonify({'error': 'Database error occurred'}), 500
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"ZIP upload error: {e}")
            return jsonify({'error': str(e)}), 500
    
    def get_all_datasets(self):
        """
        Lấy danh sách tất cả datasets
        """
        try:
            db = SessionLocal()
            try:
                datasets = db.query(Dataset).order_by(Dataset.created_at.desc()).all()
                
                result = []
                for dataset in datasets:
                    dataset_dict = dataset.to_dict()
                    # Thêm thông tin về file existence
                    dataset_dict['path_exists'] = os.path.exists(dataset.upload_path) if dataset.upload_path else False
                    result.append(dataset_dict)
                
                return jsonify({
                    'success': True,
                    'datasets': result,
                    'total': len(result)
                }), 200
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Get datasets error: {e}")
            return jsonify({'error': str(e)}), 500
    
    def get_dataset_by_id(self, dataset_id):
        """
        Lấy thông tin dataset theo ID
        """
        try:
            db = SessionLocal()
            try:
                dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
                
                if not dataset:
                    return jsonify({'error': 'Dataset not found'}), 404
                
                dataset_dict = dataset.to_dict()
                dataset_dict['path_exists'] = os.path.exists(dataset.upload_path) if dataset.upload_path else False
                
                # Thêm thông tin chi tiết về files
                if dataset.upload_path and os.path.exists(dataset.upload_path):
                    images_path = os.path.join(dataset.upload_path, 'images')
                    labels_path = os.path.join(dataset.upload_path, 'labels')
                    
                    if os.path.exists(images_path):
                        images = [f for f in os.listdir(images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
                        dataset_dict['actual_image_count'] = len(images)
                        dataset_dict['sample_images'] = images[:5]  # First 5 images
                    
                    if os.path.exists(labels_path):
                        labels = [f for f in os.listdir(labels_path) if f.endswith('.txt')]
                        dataset_dict['label_count'] = len(labels)
                
                return jsonify({
                    'success': True,
                    'dataset': dataset_dict
                }), 200
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Get dataset error: {e}")
            return jsonify({'error': str(e)}), 500
    
    def delete_dataset(self, dataset_id):
        """
        Xóa dataset
        """
        try:
            db = SessionLocal()
            try:
                dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
                
                if not dataset:
                    return jsonify({'error': 'Dataset not found'}), 404
                
                # Xóa files
                if dataset.upload_path and os.path.exists(dataset.upload_path):
                    import shutil
                    shutil.rmtree(dataset.upload_path)
                
                # Xóa record
                db.delete(dataset)
                db.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Dataset deleted successfully'
                }), 200
                
            except Exception as e:
                db.rollback()
                logger.error(f"Delete dataset error: {e}")
                return jsonify({'error': 'Failed to delete dataset'}), 500
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Delete dataset error: {e}")
            return jsonify({'error': str(e)}), 500

    def get_dataset_preview(self, dataset_id):
        """
        Lấy preview dataset với images và annotations
        """
        try:
            db = SessionLocal()
            try:
                # Get dataset info
                dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
                if not dataset:
                    return jsonify({'error': 'Dataset not found'}), 404

                # Get dataset path
                dataset_path = os.path.join(self.upload_dir, f"dataset_{dataset_id}")
                images_path = os.path.join(dataset_path, "images")
                labels_path = os.path.join(dataset_path, "labels")
                classes_file_path = os.path.join(dataset_path, "classes.txt")

                if not os.path.exists(images_path):
                    return jsonify({'error': 'Dataset images not found'}), 404

                # Read class names
                class_names = {}
                if os.path.exists(classes_file_path):
                    try:
                        with open(classes_file_path, 'r', encoding='utf-8') as f:
                            for idx, line in enumerate(f):
                                class_names[idx] = line.strip()
                    except Exception as e:
                        logger.warning(f"Error reading classes.txt for dataset {dataset_id}: {e}")
                
                # Get all images
                image_files = []
                for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
                    image_files.extend(glob.glob(os.path.join(images_path, ext)))
                    image_files.extend(glob.glob(os.path.join(images_path, ext.upper())))

                # Prepare preview data
                preview_data = []
                for img_path in image_files[:50]:  # Limit to 50 images for performance
                    img_name = os.path.basename(img_path)
                    img_name_no_ext = os.path.splitext(img_name)[0]

                    # Get corresponding label file
                    label_file = os.path.join(labels_path, f"{img_name_no_ext}.txt")

                    # Read image dimensions
                    try:
                        from PIL import Image
                        with Image.open(img_path) as img:
                            img_width, img_height = img.size
                    except Exception:
                        img_width, img_height = 640, 640  # Default

                    # Read raw label content
                    raw_label_content = None
                    if os.path.exists(label_file):
                        try:
                            with open(label_file, 'r', encoding='utf-8') as f:
                                raw_label_content = f.read()
                        except Exception as e:
                            logger.warning(f"Error reading raw label content from {label_file}: {e}")

                    # Read annotations
                    annotations = []
                    if os.path.exists(label_file):
                        try:
                            with open(label_file, 'r') as f:
                                for line in f:
                                    parts = line.strip().split()
                                    if len(parts) >= 5:
                                        class_id = int(parts[0])
                                        x_center = float(parts[1])
                                        y_center = float(parts[2])
                                        width = float(parts[3])
                                        height = float(parts[4])

                                        # Convert YOLO format to pixel coordinates
                                        x1 = int((x_center - width/2) * img_width)
                                        y1 = int((y_center - height/2) * img_height)
                                        x2 = int((x_center + width/2) * img_width)
                                        y2 = int((y_center + height/2) * img_height)

                                        annotations.append({
                                            'class_id': class_id,
                                            'class_name': class_names.get(class_id, f'class_{class_id}'),  # Map to actual class names
                                            'bbox': [x1, y1, x2, y2],
                                            'confidence': 1.0 # This is a placeholder, as YOLO labels don't typically include confidence.
                                        })
                        except Exception as e:
                            logger.warning(f"Error reading label file {label_file}: {e}")

                    # Create image URL (relative to static serving)
                    img_url = f"/static/datasets/dataset_{dataset_id}/images/{img_name}"

                    preview_data.append({
                        'image_name': img_name,
                        'image_url': img_url,
                        'image_width': img_width,
                        'image_height': img_height,
                        'annotations': annotations,
                        'raw_label_content': raw_label_content
                    })

                return jsonify({
                    'success': True,
                    'dataset': {
                        'id': dataset.id,
                        'name': dataset.name,
                        'description': dataset.description,
                        'image_count': len(image_files),
                        'preview_count': len(preview_data)
                    },
                    'images': preview_data
                }), 200

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Get dataset preview error: {e}")
            return jsonify({'error': str(e)}), 500
    
    def _extract_and_validate_zip(self, zip_path, extract_path):
        """
        Extract và validate ZIP dataset
        """
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            # Validate structure
            required_folders = ['images']
            optional_folders = ['labels']
            
            images_path = os.path.join(extract_path, 'images')
            labels_path = os.path.join(extract_path, 'labels')
            classes_path = os.path.join(extract_path, 'classes.txt')
            
            if not os.path.exists(images_path):
                return {'valid': False, 'message': 'Missing images folder'}
            
            # Count images
            images = [f for f in os.listdir(images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            if len(images) == 0:
                return {'valid': False, 'message': 'No valid images found'}
            
            # Check labels
            has_labels = os.path.exists(labels_path)
            if not has_labels:
                # Tạo labels folder và files rỗng
                os.makedirs(labels_path, exist_ok=True)
                for img in images:
                    label_name = os.path.splitext(img)[0] + '.txt'
                    with open(os.path.join(labels_path, label_name), 'w') as f:
                        pass
            
            # Tạo classes.txt nếu chưa có
            if not os.path.exists(classes_path):
                with open(classes_path, 'w') as f:
                    f.write('license_plate\n')
            
            return {
                'valid': True,
                'image_count': len(images),
                'has_labels': has_labels,
                'message': 'Dataset validated successfully'
            }
            
        except Exception as e:
            return {'valid': False, 'message': f'Validation error: {str(e)}'}
    
    def get_auto_labeler_info(self):
        """
        Lấy thông tin về auto-labeler
        """
        try:
            info = self.auto_labeler.get_model_info()
            return jsonify({
                'success': True,
                'auto_labeler': info
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
