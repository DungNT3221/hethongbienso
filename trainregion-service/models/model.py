from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, Enum, ForeignKey
from sqlalchemy.sql import func
from config.config import Base

class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    version = Column(String(50), nullable=False)
    epochs = Column(Integer, nullable=False)
    batch_size = Column(Integer, nullable=False)
    dataset_size = Column(Integer, nullable=False)
    training_time = Column(Float, nullable=False)
    map50 = Column(Float, nullable=False)
    map95 = Column(Float, nullable=False)
    model_path = Column(String(500), nullable=False)

    # New fields for approval workflow
    is_approved = Column(Boolean, default=False)
    approval_notes = Column(Text)
    dataset_id = Column(Integer, ForeignKey('datasets.id'))
    train_val_split = Column(Float, default=0.8)

    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'version': self.version,
            'epochs': self.epochs,
            'batch_size': self.batch_size,
            'dataset_size': self.dataset_size,
            'training_time': self.training_time,
            'map50': self.map50,
            'map95': self.map95,
            'model_path': self.model_path,
            'is_approved': getattr(self, 'is_approved', False),
            'approval_notes': getattr(self, 'approval_notes', None),
            'dataset_id': getattr(self, 'dataset_id', None),
            'train_val_split': getattr(self, 'train_val_split', 0.8),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
