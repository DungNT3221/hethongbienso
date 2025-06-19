import os
import shutil
from ultralytics import YOLO
from PIL import Image
import logging

class AutoLabeler:
    def __init__(self, model_path="runs/detect/train2/weights/best.pt"):
        """
        Initialize AutoLabeler với pre-trained model
        """
        self.model_path = model_path
        self.model = None
        self.confidence_threshold = 0.3
        self.logger = logging.getLogger(__name__)
        
        # Load model nếu file tồn tại
        if os.path.exists(model_path):
            try:
                self.model = YOLO(model_path)
                self.logger.info(f"Loaded model from {model_path}")
            except Exception as e:
                self.logger.error(f"Failed to load model: {e}")
                # Fallback to pretrained model
                self.model = YOLO("yolov8n.pt")
                self.logger.info("Using fallback yolov8n.pt model")
        else:
            # Sử dụng pretrained model nếu không có model custom
            self.model = YOLO("yolov8n.pt")
            self.logger.warning(f"Model file {model_path} not found, using yolov8n.pt")
    
    def process_images(self, image_files, dataset_id, method='auto', confidence_threshold=None):
        """
        Process uploaded images với method được chỉ định
        """
        if confidence_threshold:
            self.confidence_threshold = confidence_threshold
            
        if method == 'auto':
            return self._auto_label(image_files, dataset_id)
        elif method == 'template':
            return self._template_label(image_files, dataset_id)
        else:
            return self._manual_label(image_files, dataset_id)
    
    def _auto_label(self, image_files, dataset_id):
        """
        Auto-labeling sử dụng pre-trained model
        """
        dataset_path = f"uploads/dataset_{dataset_id}"
        images_path = os.path.join(dataset_path, 'images')
        labels_path = os.path.join(dataset_path, 'labels')
        
        # Tạo thư mục
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)
        
        labeled_count = 0
        total_confidence = 0.0
        
        for image_file in image_files:
            try:
                # Lưu ảnh
                image_path = os.path.join(images_path, image_file.filename)
                image_file.save(image_path)
                
                # Tạo label tự động
                confidence = self._create_auto_label(image_path, labels_path, image_file.filename)
                if confidence > 0:
                    labeled_count += 1
                    total_confidence += confidence
                    
            except Exception as e:
                self.logger.error(f"Error processing {image_file.filename}: {e}")
        
        # Tạo classes.txt
        self._create_classes_file(dataset_path)
        
        # Tính accuracy estimate
        accuracy_estimate = (total_confidence / labeled_count) if labeled_count > 0 else 0.0
        
        return {
            'dataset_id': dataset_id,
            'total_images': len(image_files),
            'labeled_images': labeled_count,
            'unlabeled_images': len(image_files) - labeled_count,
            'method': 'auto',
            'accuracy_estimate': round(accuracy_estimate, 3),
            'confidence_threshold': self.confidence_threshold
        }
    
    def _create_auto_label(self, image_path, labels_path, filename):
        """
        Tạo label file từ model prediction
        """
        try:
            # Predict
            results = self.model.predict(image_path, conf=self.confidence_threshold, verbose=False)
            
            if len(results[0].boxes) == 0:
                # Tạo file label rỗng
                label_filename = os.path.splitext(filename)[0] + '.txt'
                label_path = os.path.join(labels_path, label_filename)
                with open(label_path, 'w') as f:
                    pass  # File rỗng
                return 0.0
            
            # Tạo label file
            label_filename = os.path.splitext(filename)[0] + '.txt'
            label_path = os.path.join(labels_path, label_filename)
            
            max_confidence = 0.0
            with open(label_path, 'w') as f:
                for box in results[0].boxes:
                    confidence = box.conf[0].item()
                    if confidence > self.confidence_threshold:
                        # Convert to YOLO format
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        img_w, img_h = results[0].orig_shape[1], results[0].orig_shape[0]
                        
                        x_center = (x1 + x2) / 2 / img_w
                        y_center = (y1 + y2) / 2 / img_h
                        width = (x2 - x1) / img_w
                        height = (y2 - y1) / img_h
                        
                        # Class 0 for license_plate
                        f.write(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
                        
                        max_confidence = max(max_confidence, confidence)
            
            return max_confidence
            
        except Exception as e:
            self.logger.error(f"Error creating auto label for {filename}: {e}")
            return 0.0
    
    def _template_label(self, image_files, dataset_id, template_type='center'):
        """
        Template-based labeling
        """
        templates = {
            'center': {'x_center': 0.5, 'y_center': 0.6, 'width': 0.3, 'height': 0.15},
            'bottom': {'x_center': 0.5, 'y_center': 0.8, 'width': 0.25, 'height': 0.12}
        }
        
        template = templates.get(template_type, templates['center'])
        dataset_path = f"uploads/dataset_{dataset_id}"
        images_path = os.path.join(dataset_path, 'images')
        labels_path = os.path.join(dataset_path, 'labels')
        
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)
        
        for image_file in image_files:
            # Lưu ảnh
            image_path = os.path.join(images_path, image_file.filename)
            image_file.save(image_path)
            
            # Tạo label từ template
            label_filename = os.path.splitext(image_file.filename)[0] + '.txt'
            label_path = os.path.join(labels_path, label_filename)
            
            with open(label_path, 'w') as f:
                f.write(f"0 {template['x_center']:.6f} {template['y_center']:.6f} "
                       f"{template['width']:.6f} {template['height']:.6f}\n")
        
        self._create_classes_file(dataset_path)
        
        return {
            'dataset_id': dataset_id,
            'total_images': len(image_files),
            'labeled_images': len(image_files),
            'method': 'template',
            'template_type': template_type,
            'accuracy_estimate': 0.6  # Template accuracy estimate
        }
    
    def _manual_label(self, image_files, dataset_id):
        """
        Tạo dataset với labels rỗng cho manual labeling
        """
        dataset_path = f"uploads/dataset_{dataset_id}"
        images_path = os.path.join(dataset_path, 'images')
        labels_path = os.path.join(dataset_path, 'labels')
        
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)
        
        for image_file in image_files:
            # Lưu ảnh
            image_path = os.path.join(images_path, image_file.filename)
            image_file.save(image_path)
            
            # Tạo label file rỗng
            label_filename = os.path.splitext(image_file.filename)[0] + '.txt'
            label_path = os.path.join(labels_path, label_filename)
            with open(label_path, 'w') as f:
                pass  # File rỗng
        
        self._create_classes_file(dataset_path)
        
        return {
            'dataset_id': dataset_id,
            'total_images': len(image_files),
            'labeled_images': 0,
            'method': 'manual',
            'accuracy_estimate': 0.0
        }
    
    def _create_classes_file(self, dataset_path):
        """
        Tạo classes.txt file
        """
        classes_path = os.path.join(dataset_path, 'classes.txt')
        with open(classes_path, 'w') as f:
            f.write('license_plate\n')
    
    def get_model_info(self):
        """
        Lấy thông tin về model đang sử dụng
        """
        return {
            'model_path': self.model_path,
            'model_loaded': self.model is not None,
            'confidence_threshold': self.confidence_threshold
        }
