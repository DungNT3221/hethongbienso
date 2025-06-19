from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from config.config import Base

class PredictLog(Base):
    __tablename__ = 'predict_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    image_path = Column(String(255), nullable=False)
    result_path = Column(String(255))
    num_detections = Column(Integer)
    confidence_scores = Column(Text)
    bounding_boxes = Column(Text)
    processing_time = Column(Float)
    created_at = Column(DateTime, default=func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'model_id': self.model_id,
            'image_path': self.image_path,
            'result_path': self.result_path,
            'num_detections': self.num_detections,
            'confidence_scores': self.confidence_scores,
            'bounding_boxes': self.bounding_boxes,
            'processing_time': self.processing_time,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
