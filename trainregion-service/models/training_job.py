from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum, ForeignKey, Boolean
from sqlalchemy.sql import func
from config.config import Base

class TrainingJob(Base):
    __tablename__ = 'train_jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum('pending', 'running', 'completed', 'failed', 'stopped', name='training_status'), default='pending')

    # New fields for enhanced training
    name = Column(String(255))
    dataset_id = Column(Integer, ForeignKey('datasets.id'))
    model_type = Column(String(50), default='yolov8n')
    epochs = Column(Integer, default=100)
    batch_size = Column(Integer, default=16)
    learning_rate = Column(Float, default=0.01)
    image_size = Column(Integer, default=640)
    progress = Column(Float, default=0.0)
    current_epoch = Column(Integer, default=0)
    best_map50 = Column(Float, default=0.0)
    best_map95 = Column(Float, default=0.0)
    training_time = Column(Float, default=0.0)
    result_path = Column(String(500))

    # New fields for manual model save
    model_path = Column(String(500))
    model_saved = Column(Boolean, default=False)

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'name': self.name,
            'dataset_id': self.dataset_id,
            'model_type': self.model_type,
            'epochs': self.epochs,
            'batch_size': self.batch_size,
            'learning_rate': self.learning_rate,
            'image_size': self.image_size,
            'progress': self.progress,
            'current_epoch': self.current_epoch,
            'best_map50': self.best_map50,
            'best_map95': self.best_map95,
            'training_time': self.training_time,
            'result_path': self.result_path,
            'model_path': self.model_path,
            'model_saved': self.model_saved,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
